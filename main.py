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
from core.utils.utils import print_header, show_balances
from core.swap.swap import swap
from approve import approve_if_needed
from datetime import datetime

GTE_TOKENS = [
    Web3.to_checksum_address("0x768b22e6aaf9d0b6233b5820c8908ed820eb5b2c"),
    Web3.to_checksum_address("0xe9b6e7e7cb948e15cb6ac2d58cc05b57be7b07db"),
    Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19"),
    Web3.to_checksum_address("0xf82ff0799448630eb56ce747db840a2e02cde4d8"),
    Web3.to_checksum_address("0x8d635c4702ba38b1f1735e8e784c7265dcc0b623")
]

FDEX_ROUTER_ADDRESS = "0xA6b579684E943F7D00d616A48cF99b5147fC57A5"
FDEX_ROUTER_ABI = ROUTER_ABI

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--dex", help="Pilih DEX: GTE, fdex, atau auto", default=None)
args = parser.parse_args()

def get_rotated_router(web3):
    override = args.dex or os.getenv("DEX_OVERRIDE", "auto").lower()

    if override == "GTE":
        print("🧭 Router: GTE (Manual Override)")
        return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI), ROUTER_ADDRESS

    if override == "fdex":
        print("🧭 Router: FDEX (Manual Override)")
        return web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI), FDEX_ROUTER_ADDRESS

    use_fdex = random.choice([True, False])
    if use_fdex:
        print("🧭 Router: FDEX (Auto Random)")
        return web3.eth.contract(address=FDEX_ROUTER_ADDRESS, abi=FDEX_ROUTER_ABI), FDEX_ROUTER_ADDRESS
    else:
        print("🧭 Router: GTE (Auto Random)")
        return web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI), ROUTER_ADDRESS

def load_wallets():
    with open("private_keys.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]

def wrap_eth(web3, account, weth_address, amount_eth, gas_price_gwei):
    weth = web3.eth.contract(address=weth_address, abi=[{
        "inputs": [], "name": "deposit", "outputs": [], "stateMutability": "payable", "type": "function"
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
    print(f"🔠 Wrapping {amount_eth:.4f} ETH to WETH... tx: {tx_hash.hex()}")
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

def get_native_balance(web3, account):
    return Web3.from_wei(web3.eth.get_balance(account.address), 'ether')

def get_token_balance(web3, account, token_address):
    try:
        contract = web3.eth.contract(address=token_address, abi=[{
            "constant": True,
            "inputs": [{"name": "owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        }])
        return contract.functions.balanceOf(account.address).call()
    except Exception as e:
        print(f"⚠️  Gagal ambil saldo token {token_address[:8]}...: {e}")
        return 0

def get_onchain_tx_count(web3, address):
    try:
        return web3.eth.get_transaction_count(address)
    except Exception as e:
        print(f"❌ Gagal ambil total TX onchain: {e}")
        return None

def main():
    print_header()
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    router, router_address = get_rotated_router(web3)

    private_keys = load_wallets()
    WETH = Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19")
    gas_price_gwei = 0.1

    try:
        rounds = int(input("🔁 Berapa kali mau swap random per wallet? "))
        percent = float(input("💸 Berapa persen dari saldo token yang mau diswap tiap kali (contoh: 30)? "))
        wrap_amount = float(input("🔠 Mau wrap berapa ETH jadi WETH per wallet? (misal: 0.01): "))
    except ValueError:
        print("❌ Input tidak valid. Harus angka.")
        return

    if not 0 < percent <= 100:
        print("❌ Persen harus antara 0-100.")
        return

    swap_fraction = percent / 100

    for idx, pk in enumerate(private_keys, start=1):
        account = Account.from_key(pk)
        print(f"\n{'='*50}\n💼 Wallet #{idx}: {account.address}\n{'='*50}")
        for token in GTE_TOKENS:
            balance = get_token_balance(web3, account, token)
            if balance > 0:
                try:
                    contract = web3.eth.contract(address=token, abi=[{
                        "constant": True,
                        "inputs": [],
                        "name": "symbol",
                        "outputs": [{"name": "", "type": "string"}],
                        "type": "function"
                    }])
                    name = contract.functions.symbol().call()
                except:
                    name = token[:6]
                print(f" - {name}: {balance:.4f}")

        native_eth = get_native_balance(web3, account)
        print(f"🔠 Saldo native ETH kamu: {native_eth:.4f}")

        onchain_total = get_onchain_tx_count(web3, account.address)
        if onchain_total is not None:
            print(f"📦 Total TX on-chain: {onchain_total}")

        if native_eth > wrap_amount:
            wrap_eth(web3, account, WETH, wrap_amount, gas_price_gwei)

        total_tx = 0

        for i in range(rounds):
            router, router_address = get_rotated_router(web3)
            print(f"\n🔁 SWAP RANDOM KE-{i + 1}")
            show_balances(web3, account)

            tokens_with_balance = [
                token for token in GTE_TOKENS if get_token_balance(web3, account, token) > 0
            ]

            if len(tokens_with_balance) == 0:
                print("⚠️ Tidak ada token dengan saldo. Skip.")
                continue

            token_in = random.choice(tokens_with_balance)
            token_out = random.choice([t for t in GTE_TOKENS if t != token_in])
            amt = get_token_balance(web3, account, token_in)

            print(f"🎯 Swap random: {token_in[:6]}... → {token_out[:6]}...")

            try:
                approve_if_needed(web3, account, token_in, router_address, amt * swap_fraction, gas_price_gwei)
            except Exception as e:
                send_telegram(
                    f"❌ *Approve Gagal!*\n"
                    f"📄 Error: `{e}`"
                )
                continue

            try:
                tx = swap(web3, account, router, token_in, token_out, amt * swap_fraction, gas_price_gwei)
            except Exception as e:
                send_telegram(
                    f"❌ *Swap Gagal!*\n"
                    f"📄 Error: `{e}`"
                )
                continue

            if tx:
                total_tx += 1
                tx_link = f"https://www.oklink.com/megaeth-testnet/tx/{tx.hex()}"
                router_name = "Bronto (FDEX)" if router_address.lower() == FDEX_ROUTER_ADDRESS.lower() else "GTE ROUTER (GTE)"
                try:
                    symbol_in = web3.eth.contract(address=token_in, abi=[{"name": "symbol", "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"}]).functions.symbol().call()
                except:
                    symbol_in = token_in[:6]
                try:
                    symbol_out = web3.eth.contract(address=token_out, abi=[{"name": "symbol", "outputs": [{"type": "string"}], "inputs": [], "stateMutability": "view", "type": "function"}]).functions.symbol().call()
                except:
                    symbol_out = token_out[:6]

                send_telegram(
                    f"✨ *Swap Berhasil!*\n"
                    f"💼 Wallet: {account.address}\n"
                    f"🔁 Pair: {symbol_in} → {symbol_out}\n"
                    f"💼 DEX: {router_name}\n"
                    f"💰 Amount: {amt * swap_fraction / 1e18:.6f} {symbol_in}\n"
                    f"🔗 TX: [Klik di sini]({tx_link})\n"
                    f"📊 Total TX Hari Ini: {total_tx}\n"
                    f"📦 Total TX (Onchain): {onchain_total}\n"
                    f"⛽ Gas Estimasi: {gas_price_gwei} Gwei"
                )

            time.sleep(random.uniform(3, 8))

        print(f"\n✅ Wallet {account.address} selesai. Total transaksi hari ini: {total_tx}")

        if idx < len(private_keys):
            wait = random.randint(10, 25)
            print(f"⏳ Menunggu {wait} detik sebelum lanjut ke wallet berikutnya...")
            time.sleep(wait)

    print("\n🎉 Semua wallet selesai swap hari ini.")
    print("🤖 Bot by SAHME — GTE Testnet domination started.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Dibatalkan oleh user.")
