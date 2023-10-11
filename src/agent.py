from datetime import datetime
import asyncio
from .api import pull_25_tweets, save_hour, load_last_hour
from .Check_address import check_addresses
from .remove_duplicates_addresses import remove_duplicate_addresses

from forta_agent import (
    Finding,
    FindingSeverity,
    FindingType,
    EntityType
)

async def run_twitter():
    addresses_in_tweets = []
    urls_in_tweets = []
    await pull_25_tweets()
    await check_addresses()
    new_addresses, new_urls = await remove_duplicate_addresses()
   
    
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

    if new_urls is not None:
         for _, row in new_urls.iterrows():
                matching_url = {
                    "url_found": row.iloc[2],
                    "tweet_date": row.iloc[0],
                    "tweet_owner": row.iloc[4],
                    "tweet_url": row.iloc[5],
                    "tweet_text": row.iloc[7],
                    "Malicious_url" : row.iloc[3]
                }
                urls_in_tweets.append(matching_url)


    
    return addresses_in_tweets, urls_in_tweets

def handle_block(block_event):
    findings = []
    current_hour = datetime.now().hour
    print('current hour:', current_hour)
    last_hour = load_last_hour()
    print('last hour: ',  last_hour)
    if current_hour % 2 != 0 and current_hour != last_hour:
        addresses_in_tweets, urls_in_tweets =  asyncio.run(run_twitter())
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
                            "labels":  [{
                                        "entityType": EntityType.Address,
                                        "entity": f"{matching_tweet['address_found']}",
                                        "label": "attacker",
                                        "confidence": 0.8,
                                             }]
                        }
                    )
                )
        if urls_in_tweets: 
            for matching_url in urls_in_tweets:
                findings.append(
                    Finding(
                        {
                            "name": "Potential Malicious URL",
                            "description": f"URL {matching_url['Malicious_url']} was mentioned in a Tweet",
                            "alert_id": "FORTA-1",
                            "protocol": "ethereum",  
                            "type": FindingType.Suspicious,
                            "severity": FindingSeverity.Low,
                            "metadata": {
                                "Twitter_Mentioned_URL": matching_url['Malicious_url'],
                                "Date_Tweeted": matching_url['tweet_date'],
                                "Account_from": matching_url['tweet_owner'],
                                "Tweet_URL": matching_url['tweet_url'],
                                "tweet_text": matching_url['tweet_text'],
                                             },
                            "labels":  [{
                                        "entityType": EntityType.Url,
                                        "entity": f"{matching_url['Malicious_url']}",
                                        "label": "Pishing URL",
                                        "confidence": 1,
                                             }]
                        }
                    )
                )

   
    return findings
