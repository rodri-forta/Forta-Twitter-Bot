texto = "victim: 0xa14ea77bb57487f73459f06A5ad85F509492FEC3  scammers: 0x0000f0D34d51D23B0dd75A6b720c7F4f10430000 0x47d3503D499247AfA3E9A0A08CBb8C97088Ee0b2 0x40665350bcF25f602aa21b6e98d590C9F6E5Fcf4"

import re

import re

def extract_addresses(text):
    # Buscar todas las direcciones y posibles ocurrencias de 'victim' antes de ellas
    pattern = r'\b(?i)victim\s*:?\s*(0x[a-fA-F0-9]{40})\b|\b(0x[a-fA-F0-9]{40})\b'
    matches = re.findall(pattern, text)

    valid_addresses = []
    for victim_match, address_match in matches:
        # Si victim_match está vacío, la dirección no está precedida por 'victim'
        if not victim_match:
            valid_addresses.append(address_match)

    return valid_addresses

print(extract_addresses(texto))