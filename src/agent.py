from datetime import datetime
import asyncio
from .api import pull_25_tweets, save_hour, load_last_hour
from .Check_address import check_addresses
from .remove_duplicates_addresses import remove_duplicate_addresses

from forta_agent import (
    Finding,
    FindingSeverity,
    FindingType,
   
)

async def run_twitter():
    addresses_in_tweets = []
    await pull_25_tweets()
    await check_addresses()
    new_addresses = await remove_duplicate_addresses()
   
    
    if new_addresses is not None:
        if len(new_addresses) > 0:
            for _, row in new_addresses.iterrows():
                matching_tweet = {
                    "address_found": row.iloc[2],
                    "tweet_date": row.iloc[0],
                    "tweet_owner": row.iloc[3],
                    "tweet_url": row.iloc[4],
                    "tweet_text": row.iloc[7],
                    "Original_Smart_contract" : row.iloc[8]
                }
                addresses_in_tweets.append(matching_tweet)

            return addresses_in_tweets

def handle_block(block_event):
    findings = []
    current_hour = datetime.now().hour
    print(current_hour)
    # Load the next token and timestamp from file if they exist
    last_hour , last_timestamp = load_last_hour()
    print(last_hour)
    if current_hour % 2 == 0 and current_hour != last_hour:
     
        addresses_in_tweets =  asyncio.run(run_twitter())
        save_hour(current_hour)
        if addresses_in_tweets:          

            for matching_tweet in addresses_in_tweets:
                findings.append(
                    Finding(
                        {
                            "name": "Potential Malicious Address",
                            "description": f"Address {matching_tweet['address_found']} was mentioned in a Tweet",
                            "alert_id": "FORTA-1",
                            "protocol": "ethereum",  # Corrected the spelling
                            "type": FindingType.Suspicious,
                            "severity": FindingSeverity.Low,
                            "metadata": {
                                "Twitter_Mentioned_Account": matching_tweet['address_found'],
                                "Date_Tweeted": matching_tweet['tweet_date'],
                                "Account_from": matching_tweet['tweet_owner'],
                                "Tweet_URL": matching_tweet['tweet_url'],
                                "tweet_text": matching_tweet['tweet_text'],
                                             },
                        }
                    )
                )

   
    return findings