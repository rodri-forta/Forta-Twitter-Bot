from web3 import Web3
from dotenv import load_dotenv
import csv
import requests
import pandas as pd
import re
import time 
import json
import pandas as pd
from datetime import datetime, timedelta
import requests
from hexbytes import HexBytes




with open('secrets.json', 'r') as secrets_file:
    secrets = json.load(secrets_file)

BSC_SCAN_TOKEN = secrets.get("BSC_SCAN_TOKEN")
ETH_SCAN_TOKEN = secrets.get("ETH_SCAN_TOKEN")
INFURIA_TOKEN = secrets.get("INFURIA_TOKEN")
QUICKNODE_TOKEN = secrets.get("QUICKNODE_TOKEN")

ETH_RPC = secrets.get('MAINNET_INFURA_RPC_ENDPOINT')
BSC_RPC = secrets.get('BSC_RPC_ENDPOINT')





rpc_endpoint_address_eth = ETH_RPC
w3_eth = Web3(Web3.HTTPProvider(rpc_endpoint_address_eth))
w3_eth.manager.request_blocking

rpc_endpoint_address_bsc = BSC_RPC
w3_bsc = Web3(Web3.HTTPProvider(rpc_endpoint_address_bsc))
w3_bsc.manager.request_blocking
def is_contract_eth(address) -> bool:
    """
    this function determines whether address is a contract
    :return: is_contract: bool
    """
    if address is None:
        return True
    code = w3_eth.eth.get_code(Web3.toChecksumAddress(address))
    return code != HexBytes('0x')

def is_contract_bsc(address) -> bool:
    """
    this function determines whether address is a contract
    :return: is_contract: bool
    """
    if address is None:
        return True
    code = w3_bsc.eth.get_code(Web3.toChecksumAddress(address))
    return code != HexBytes('0x')



def check_address_type_ETH(address):
    contract = is_contract_eth(address)
    
    if contract == True:
       return 'ETH_SMART_CONTRACT'
    else:
        return 'ETH_EOA'

def check_address_type_BSC(address):
    contract = is_contract_bsc(address)
    
    if contract == True:
        return 'BSC_SMART_CONTRACT'
    else:
        return 'BSC_EOA'


def get_contract_deployer_BSC(BSC_scontract):

    # Define a limit for the number of transactions to retrieve
    transaction_limit = 1

    # BscScan API endpoint to get transaction list for an address
    bscscan_url = f"https://api.bscscan.com/api?module=account&action=txlist&address={BSC_scontract}&startblock=0&endblock=99999999&page=1&offset={transaction_limit}&sort=asc&apikey={BSC_SCAN_TOKEN}"

    # Send a GET request to the BscScan API
    response = requests.get(bscscan_url)

    if response.status_code == 200:
        data = response.json()
        transactions = data["result"]
            
        # Iterate through transactions and write them to the CSV file
        for tx in transactions:
            if tx['to'] == "":
                deployer = tx['from']
            else: 
                deployer = "none"
    else:
        print("Failed to fetch data from BscScan API.")
    
    return deployer
def get_contract_deployer_ETH(ETH_scontract):

    contract_address = ETH_scontract
    # Define a limit for the number of transactions to retrieve
    transaction_limit = 1

    # BscScan API endpoint to get transaction list for an address
    bscscan_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_scontract}&startblock=0&endblock=99999999&page=1&offset={transaction_limit}&sort=asc&apikey={ETH_SCAN_TOKEN}"

    # Send a GET request to the BscScan API
    response = requests.get(bscscan_url)

    if response.status_code == 200:
        data = response.json()
        transactions = data["result"]
            
        # Iterate through transactions and write them to the CSV file
        for tx in transactions:
            if tx['to'] == "":
                deployer = tx['from']
            else: 
                deployer = "none"
    else:
        print("Failed to fetch data from BscScan API.")
    
    return deployer




def custom_date_parser(date_str):
    # Convert to datetime using the appropriate format
    return datetime.strptime(date_str, '%m/%d/%Y')

async def check_addresses():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('result_data.csv', header=None, names=['Date','Type','Address','Account','TweetURL','Chain ID','Threat category','Comment'])

    # Apply the custom date parser to the 'Date' column
    df['Date'] = df['Date'].iloc[1:].apply(custom_date_parser)
    # Calculate the date from 7 days ago
    three_days_ago = datetime.now() - timedelta(days=30)

    # Filter rows where the 'Date' is greater than seven_days_ago
    filtered_df = df[df['Date'] > three_days_ago]


    ## Initialize an empty list to store the extracted data
    data = []

    for index, row in filtered_df.iterrows():
        if index >= 1:  # Start from row 2
                address = row['Address']
                print(address.lower(),index)
                checksum_address = Web3.toChecksumAddress(address.lower()) # Convert to checksum address
                chain = row['Chain ID'] if pd.notna(row['Chain ID']) else ''
                tag = ''
                
                # Add a time delay of 1 second between processing rows
                time.sleep(1)  # Adjust the delay time as needed
                
                if check_address_type_ETH(checksum_address) == 'ETH_SMART_CONTRACT':
                    tag = 'Smart Contract'
                    chain = '1'
                    deployer_EOA =  get_contract_deployer_ETH( checksum_address)
                    print('Smart contract: ' + deployer_EOA)
                    if deployer_EOA != 'none':
                        with open('deployer_addresses.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pd.to_datetime(row['Date']).strftime('%m/%d/%Y'),'Address', deployer_EOA,row['Account'],row['TweetURL'],chain,'', row['Comment'], checksum_address])
                    else:
                        tag = 'Smart Contract -NO_ADDRESS-'
                elif  check_address_type_BSC( checksum_address) == 'BSC_SMART_CONTRACT':
                    tag = 'Smart Contract'
                    chain = '56'
                    deployer_EOA = get_contract_deployer_BSC( checksum_address)
                    print('Smart contract: ' + deployer_EOA)
                    if deployer_EOA != 'none':
                        with open('deployer_addresses.csv', 'a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([pd.to_datetime(row['Date']).strftime('%m/%d/%Y'),'Address', deployer_EOA,row['Account'],row['TweetURL'],chain,'', row['Comment'], checksum_address])
                    else:
                        tag = 'Smart Contract -NO_ADDRESS-'
                else : 
                    tag = 'Address'
                    print(tag)
                    chain = row['Chain ID']         
                
                # Append data to the list
                data.append({
                    'Date': pd.to_datetime(row['Date']).strftime('%m/%d/%Y'),
                    'Type': tag,
                    'Address': row['Address'],
                    'Account': row['Account'],
                    'TweetURL': row['TweetURL'],
                    'Chain ID': chain,
                    'Threat category': '',
                    'Comment': row['Comment'],
                    'Smart contract': ''
                })
            

    # Create a new DataFrame from the extracted data
    result_df = pd.DataFrame(data)

    result_df.to_csv('end_process.csv', mode='a', header= False, index=False)



