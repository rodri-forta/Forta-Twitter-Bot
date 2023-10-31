# Forta Twitter Bot 

## Description

 Forta Twitter Bot is designed to analyze tweets from verified sources and identify addresses related to scams. It flags these addresses within the Forta Network, contributing to a safer and more secure social media environment.

Every 2 hours the bot will make a call to Twitter API asking for 25 tweets from a list of virified sources related to Web3 alerts, resulting in a 9.000 month amount of analyzed tweets. 

Each tweet will be parced into a extract_addresses() function. This function will recibe:
     . Date: The date is formatted as 'MM/DD/YYYY' and is obtained from the 'Date' column.
     . Type: The entry type is 'Address.'
     . Address: The specific address information is contained within this field.
     . Account: This field contains information related to an account, sourced from the 'Account' column.
     . TweetURL: The URL of a tweet is stored here.

The result will be an empty array if there are no addresses in the tweet 
or an array with the Address, Date and account who tweeted. In V1 addresses will not be categorized, just flagged as mention in twitter.


Version will incorpoarate ChatGPT to analyse the Tweet content and flagged the type of Scam modifying labels to have  Address, Date,  Account who tweeted and Scam category, tha could be on of the following: 
Ice phishing
Soft rug pull
Protocol attack 
End-user attack
Address poisoning 
Hard rug pull.

## Supported Chains

- Bot will be using Etherium Chain to set the 2 hours trigger to make call for the Twitter API.


## Alerts

The FortaGuard Twitter Flagged Detection Bot fires the following type of alert:

- SCAMMER ADDRESS
  - This alert is triggered when find_crypto_addresses() returns an array with a new Address and will have the following format: 

 {"Account_from":"@BeosinAlert","Date_Tweeted":"10/11/2023","Tweet_URL":"https://twitter.com/BeosinAlert/status/1711930957107007642","Twitter_Mentioned_Account":"0x281b8cb2AE64cd14501fc7Bcd2545be2836B173D","tweet_text":"$FSL on BNB Chain rugged, the deployer profited ~$1.68M.  Contract: 0x8923881e8cAe6684C2bB84D69aE88A9bbbEC8d5a  The deployer  0x281b8cb2AE64cd14501fc7Bcd2545be2836B173D minted 100M $FSL at the creation of the contract.   The 0x281b address has then sent 97M $FSL to… https://t.co/UyfYg6Oyu1 https://t.co/wv0AGsoBeQ"}

- MALICIOUS URLS
  - This alert is triggered when find_malicious_url() returns an array with new malicious URLS and will have the following format:
  
  {"Account_from":"@CertiKAlert","Date_Tweeted":"10/13/2023","Tweet_URL":"https://twitter.com/CertiKAlert/status/1712817053176885403","Twitter_Mentioned_URL":"https://www.drop-nft.website/","tweet_text":"#CertiKSkynetAlert 🚨  Beware of a fake NFT airdrop being promoted on X  Do not interact with hxxps://www.drop-nft.website/  Site connects to a phishing contract created yesterday  https://t.co/Hc7OIcNUDA"}
  
