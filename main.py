import time
import random
import requests
import os
import sys
import argparse
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI

GTE_TOKENS = [
    Web3.to_checksum_address("0x768b22e6aaf9d0b6233b5820c8908ed820eb5b2c"),  # GTE
    Web3.to_checksum_address("0xe9b6e7e7cb948e15cb6ac2d58cc05b57be7b07db"),  # MGTE
    Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19"),  # WETH
    Web3.to_checksum_address("0xf82ff0799448630eb56ce747db840a2e02cde4d8"),  # tkWBTC
    Web3.to_checksum_address("0x8d635c4702ba38b1f1735e8e784c7265dcc0b623")   # USDC
]
from core.utils.utils import print_header, show_balances
from core.swap.swap import swap
from approve import approve_if_needed

# Bronto (FDEX) Router
FDEX_ROUTER_ADDRESS = "0xA6b579684E943F7D00d616A48cF99b5147fC57A5"
FDEX_ROUTER_ABI = ROUTER_ABI  # Diasumsikan kompatibel

load_dotenv()

# Strategi pemilihan router: bisa override lewat argumen CLI atau .env
from datetime import datetime

# CLI argumen
parser = argparse.ArgumentParser()
parser.add_argument("--dex", help="Pilih DEX: uniswap, fdex, atau auto", default=None)
args = parser.parse_args()

def get_rotated_router(web3):
    override = args.dex or os.getenv("DEX_OVERRIDE", "auto").lower()

    if override == "uniswap":
        print("🧭 Router: UNISWAP (Manual Override)")
        return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI), ROUTER_ADDRESS

    if override == "fdex":
        print("🧭 Router: FDEX (Manual Override)")
        return web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI), FDEX_ROUTER_ADDRESS

    # Mode auto: random per swap
    use_fdex = random.choice([True, False])
    if use_fdex:
        print("🧭 Router: FDEX (Auto Random)")
        return web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI), FDEX_ROUTER_ADDRESS
    else:
        print("🧭 Router: UNISWAP (Auto Random)")
        return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI), ROUTER_ADDRESS

def load_wallets():
    with open("private_keys.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def wrap_eth(web3, account, weth_address, amount_eth, gas_price_gwei):
    weth = web3.eth.contract(address=weth_address, abi=[{
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }])
    tx = weth.functions.deposit().build_transaction({
        'from': account.address,
        'value': Web3.to_wei(amount_eth, 'ether'),
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 100000,
        'gasPrice': Web3.to_wei(gas_price_gwei, 'gwei')
    })
    signed = web3.eth.account.sign_transaction(tx, account.key)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"💠 Wrapping {amount_eth:.4f} ETH to WETH... tx: {tx_hash.hex()}")
    return tx_hash.hex()

def send_telegram(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload)
    except Exception:
        pass

