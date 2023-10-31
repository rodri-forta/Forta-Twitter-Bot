import pandas as pd
import re
from datetime import datetime, timedelta

def process_tweets():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('tweets_unique.csv', header=None, names=['ID', 'Account', 'Tweet', 'Date', 'TweetURL'])


    def custom_date_parser(date_str):
        # Extract the date and time part without milliseconds
        date_str = date_str[:-5]
        # Convert to datetime using the appropriate format
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    
    def https_converter(url):
    # Check if the URL starts with "hxxp://" (case insensitive)
        if url.lower().startswith("hxxp://"):
            # Replace "hxxp://" with "http://"
            return "http://" + url[7:]
        # Check if the URL starts with "hxxps://" (case insensitive)
        elif url.lower().startswith("hxxps://"):
            # Replace "hxxps://" with "https://"
            return "https://" + url[8:]
        
        return url

    
    # Regular expression to find "hxxp" links
    url_pattern = re.compile(r'hxxp\S+')


    # Apply the custom date parser to the 'Date' column
    df['Date'] = df['Date'].iloc[1:].apply(custom_date_parser)
    # Calculate the date from 7 days ago
    three_days_ago = datetime.now() - timedelta(days=3)

    # Filter rows where the 'Date' is greater than seven_days_ago
    filtered_df = df[df['Date'] > three_days_ago]

    # Initialize an empty list to store the extracted data
    data = []

    # Initialize an empty list to store the extracted data
    urls = []

    # Define a function to extract addresses from a text
    def extract_addresses(text):
        return re.findall(r'\b0x[a-fA-F0-9]{40}\b', text)

    # Iterate through each row of the DataFrame
    for index, row in filtered_df.iterrows():
        tweet_addresses = extract_addresses(row['Tweet'])
        hxxp_links = re.findall(url_pattern, row['Tweet'])
        if tweet_addresses:
            for address in tweet_addresses:
                # Determine the Chain ID based on the tweet content (case insensitive)
                if 'ethereum' in row['Tweet'].lower() or 'eth' in row['Tweet'].lower():
                    chain_id = '1'
                elif 'bsc' in row['Tweet'].lower() or 'Binance' in row['Tweet'].lower():
                    chain_id = '56'
                else:
                    chain_id = ''
                
                # Check if a Tweet URL is present
                tweet_url = row['TweetURL'] if pd.notna(row['TweetURL']) else ''
                
                # Append data to the list
                data.append({
                    'Date': pd.to_datetime(row['Date']).strftime('%m/%d/%Y'),
                    'Type': 'Address',
                    'Address': address,
                    'Account': row['Account'],
                    'TweetURL': tweet_url,
                    'Chain ID': chain_id,
                    'Threat category': '',
                    'Comment': row['Tweet'],
                    
                })
        elif hxxp_links:
            for hxxp_link in hxxp_links:
                 # Check if a Tweet URL is present
                tweet_url = row['TweetURL'] if pd.notna(row['TweetURL']) else ''
                # Append data to the list
                urls.append({
                    'Date': pd.to_datetime(row['Date']).strftime('%m/%d/%Y'),
                    'Type': 'URL',
                    'URL_found' :  hxxp_link,
                    'Malicious_URL': https_converter(hxxp_link),                   
                    'Account': row['Account'],
                    'TweetURL': tweet_url,                  
                    'Threat_category': 'Phishing URL',
                    'Tweet': row['Tweet'],
                })



    # Create a new DataFrame from the extracted data
    result_df = pd.DataFrame(data)
    result_url = pd.DataFrame(urls)

    result_df.to_csv('result_data.csv', mode='w',header=False, index=False)
    result_url.to_csv('result_urls.csv', mode='w',header=True, index=False) 
