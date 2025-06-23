
from web3 import Web3

RPC_URL = "https://carrot.megaeth.com/rpc"
ROUTER_ADDRESS = Web3.to_checksum_address("0x2e0ed91bb2b1b74d5b91f51ea99f05b2f5e35a85")

ROUTER_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [
            {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

BASE_TOKEN = Web3.to_checksum_address("0x768b22fc580d05fbdfefcfd7e462163832faca52")

GTE_TOKENS = [
    Web3.to_checksum_address("0x768b22fc580d05fbdfefcfd7e462163832faca52"),  # GTE
    Web3.to_checksum_address("0xe9b6e75c243b6100ffcb1c66e8f78f96feea727f"),  # USD
    Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19")   # ETH (WETH-style)
]
