# Forta Twitter Bot 

## Description

 Forta Twitter Bot is designed to analyze tweets from verified sources and identify addresses related to scams. It flags these addresses within the Forta Network, contributing to a safer and more secure social media environment.

Every 2 hours the bot will make a call to Twitter API asking for 25 tweets from a list of virified sources related to Web3 alerts, resulting in a 9.000 month amount of analyzed tweets. 

Each tweet will be parced into a find_crypto_addresses() function. This function will recibe:
  . The tweet text (String)
  . Date Tweeted (Unix Timestamp)
  . Account that Tweeted (String)
  

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

  { 
    Twitter_Mentioned_Account: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e", 
    Date_Tweeted: 1690389639,
    Account_from : @web3alertsexample
  }



## Test Data

To verify the behavior of the FortaGuard Twitter Flagged Detection Bot, you can input the text of the tweets of the following tweets:

### Text needed asuming Date: 1695676631
- https://twitter.com/CertiKAlert/status/1659061191363248128
        "#CertiKSkynetAlert 🚨
        We have detected suspicious activity on EOA: 0xACE5Ef13E0b4Fa2bEAac957408d6D0936227C559
        Revoke permissions if you have unintentionally given the EOA access to your tokens
        #IcePhish
        See more about this incident here 👇
        https://skynet.certik.com/alerts/security/e273ed42-3b77-43c0-98ef-334d5b12a9d1
        Stay safe!"


### Text needed asuming Date: 1695689639

- https://twitter.com/CertiKAlert/status/1659072036474433537
        "#CertiKSkynetAlert 🚨
        We have detected suspicious activity on EOA: 0x82242F63946c6198Ec5bdf765bB013995195A586
        Revoke permissions if you have unintentionally given the EOA access to your tokens.
        #IcePhish
        See more about this incident here 👇
        https://skynet.certik.com/alerts/security/68dc74da-a52d-4c2c-bfda-f875c8f32230
        Stay safe!"

## Test should emit two alerts with the following tags: 

{ 
    Twitter_Mentioned_Account: "0x82242F63946c6198Ec5bdf765bB013995195A586", 
    Date_Twitted: 1695676631,
    Account_from : @CertiKAlert
  }


{ 
    Twitter_Mentioned_Account: "0xACE5Ef13E0b4Fa2bEAac957408d6D0936227C559", 
    Date_Tweeted: 1695689639,
    Account_from : @CertiKAlert
  }