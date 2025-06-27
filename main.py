import time
import random
import requests
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI, GTE_TOKENS
from core.utils.utils import print_header, show_balances, get_token_balance
from core.swap.swap import swap
from approve import approve_if_needed

# Bronto (FDEX) Router
FDEX_ROUTER_ADDRESS = "0xA6b579684E943F7D00d616A48cF99b5147fC57A5"
FDEX_ROUTER_ABI = ROUTER_ABI  # Diasumsikan kompatibel, akan dites di bawah

load_dotenv()

def test_fdex_router_compatibility(web3):
    print("\n🔍 Menguji kompatibilitas ABI Bronto Router...")
    try:
        router = web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI)
        dummy_tx = router.functions.swapExactTokensForTokens(
            10**18,
            0,
            ["0x0000000000000000000000000000000000000001", "0x0000000000000000000000000000000000000002"],
            "0x000000000000000000000000000000000000dead",
            web3.eth.get_block("latest")['timestamp'] + 300
        ).build_transaction({
            'from': "0x000000000000000000000000000000000000dead",
            'nonce': 0,
            'gas': 200000,
            'gasPrice': web3.to_wei(1, 'gwei')
        })
        print("✅ FDEX Router kompatibel dengan ABI UniswapV2")
    except Exception as e:
        print("❌ FDEX Router kemungkinan tidak kompatibel dengan ABI UniswapV2")
        print("Error:", e)

def get_random_router(web3):
    choice = random.choice(["uniswap", "fdex"])
    if choice == "uniswap":
        print("🧭 Router: UNISWAP")
        return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI), ROUTER_ADDRESS
    else:
        print("🧭 Router: FDEX")
        return web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI), FDEX_ROUTER_ADDRESS

# Fungsi main tetap seperti sebelumnya, hanya perlu memanggil test_fdex_router_compatibility() di awal

def main():
    print_header()
    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    test_fdex_router_compatibility(web3)
    
    # ...lanjutan fungsi main tidak berubah...
