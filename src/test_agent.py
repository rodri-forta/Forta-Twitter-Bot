from typing import List
from unittest.mock import Mock

from agent import find_crypto_addresses
tweet = """$BALD rugged for ~5,000 $ETH (worth ~$9.28M).

The deployer added a total of 6,077 $ETH liquidity and removed 11,077 $ETH.

$BALD address:
0x27D2DECb4bFC9C76F0309b8E88dec3a601Fe25a8"""

class TestFlashLoanDetector:
    def test_returns_finding_if_it_sees_a_crypto_address(self):
        findings = find_crypto_addresses(tweet)
        assert len(findings) == 1
