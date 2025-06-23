# Konfigurasi jaringan GTE testnet

RPC_URL = "https://carrot.megaeth.com/rpc"

# Router GTE DEX
ROUTER_ADDRESS = "0x2e0ed91bb2b1b74d5b91f51ea99f05b2f5e35a85"

# ABI minimal untuk fungsi swap
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

# Token utama
BASE_TOKEN = "0x768b22fc580d05fbdfefcfd7e462163832faca52"  # GTE

# Semua token untuk auto swap
GTE_TOKENS = [
    "0x768b22fc580d05fbdfefcfd7e462163832faca52",  # GTE
    "0xe9b6e75c243b6100ffcb1c66e8f78f96feea727f",  # USD
    "0xfaf334e157175ff676911adcf0964d7f54f2c424",  # tkUSD
    "0x073973ccc35761d7ddd48f0c6555914852671d17",  # DOUGH
    "0x10a6be7d23989d00d528e68cf8051d095f741145",  # MEGA
    "0xfb1e310fee8f03844551ad3a62d55e7d0ab60e9e",  # MegaBunny
    "0x10a4141bccfc69be90d2d2af058138876cce1ef8",  # TRIBO
]
