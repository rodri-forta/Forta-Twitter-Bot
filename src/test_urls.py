import re
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

text = "@CertiKAlert,#CertiKSkynetAlert 🚨  Beware of a fake Arbitrum airdrop posted on social media   Do not interact with hxxps://arb.base-eth.net/?invite=twitter  Stay vigilant! https://t.co/TqRAR3nrbi,2023-10-10T23:48:58.000Z"
url_pattern = re.compile(r'hxxp\S+')
result = re.findall(url_pattern, text)
for link in result:
     result2 = https_converter(link)
     print(result2)



text2 = "Update: HTX/Huobi just sent them a whitehat bounty of 250 ETH ($410K) along with this message 0x481cc79ee51b417ecfbdcfaa21cefd5b91bc8c2b, 0x481cc79ee51b417ecfbdcfaa21cefd5b91bc8c2c"
def extract_addresses(text):
        return re.findall(r'\b0x[a-fA-F0-9]{40}\b', text)


result =  extract_addresses(text2)
print(result)