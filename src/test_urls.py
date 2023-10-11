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