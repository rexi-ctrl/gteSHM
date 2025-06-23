# Konfigurasi jaringan GTE testnet

RPC_URL = "https://rpc.gtexample.com"  # Ganti dengan RPC GTE Testnet kamu
ROUTER_ADDRESS = "0xYourRouterAddressHere"

# Gunakan ABI dari router di GTE testnet
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

# Token utama (misal GTE)
BASE_TOKEN = "0xBaseTokenAddress"

# Semua token yang digunakan dalam swap
GTE_TOKENS = [
    "0xBaseTokenAddress",    # GTE
    "0xUSDTokenAddress",     # USD
    "0xDOUGHTokenAddress",   # DOUGH
    "0xTKUSDTokenAddress",   # tkUSD
    # Tambahkan token lainnya jika ada
]
