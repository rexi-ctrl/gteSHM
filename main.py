
import time
import random
from web3 import Web3
from eth_account import Account
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI, GTE_TOKENS
from core.utils.utils import print_header, show_balances, get_token_balance
from core.swap.swap import swap
from approve import approve_if_needed
from wrap_eth import wrap_eth


def load_wallets():
    with open("private_keys.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]


def get_native_balance(web3, account):
    return Web3.from_wei(web3.eth.get_balance(account.address), 'ether')


def main():
    print_header()
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    router = web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
    private_keys = load_wallets()
    WETH = Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19")

    try:
        rounds = int(input("🔁 Berapa kali mau swap random per wallet? "))
        percent = float(input("💸 Berapa persen dari saldo token yang mau diswap tiap kali (contoh: 30)? "))
        wrap_amount = float(input("💠 Mau wrap berapa ETH jadi WETH per wallet? (misal: 0.01): "))
    except ValueError:
        print("❌ Input tidak valid. Harus angka.")
        return

    if not 0 < percent <= 100:
        print("❌ Persen harus antara 0-100.")
        return

    swap_fraction = percent / 100

    for idx, pk in enumerate(private_keys, start=1):
        account = Account.from_key(pk)
        print(f"\n{'='*50}\n👛 Wallet #{idx}: {account.address}\n{'='*50}")
        show_balances(web3, account)

        native_eth = get_native_balance(web3, account)
        print(f"💠 Saldo native ETH kamu: {native_eth:.4f}")

        if native_eth > wrap_amount:
            wrap_eth(web3, account, WETH, wrap_amount)

        total_tx = 0

        for i in range(rounds):
            print(f"\n🔁 SWAP RANDOM KE-{i + 1}")
            show_balances(web3, account)

            tokens_with_balance = [
                token for token in GTE_TOKENS
                if get_token_balance(web3, account, token) > 0
            ]

            if len(tokens_with_balance) == 0:
                print("⚠️ Tidak ada token dengan saldo. Skip.")
                continue
            elif len(tokens_with_balance) == 1:
                token_in = tokens_with_balance[0]
                token_out = random.choice([t for t in GTE_TOKENS if t != token_in])
            else:
                token_in = random.choice(tokens_with_balance)
                token_out = random.choice([t for t in GTE_TOKENS if t != token_in])

            amt = get_token_balance(web3, account, token_in)
            print(f"🎯 Swap random: {token_in[:6]}... → {token_out[:6]}...")

            approve_if_needed(web3, account, token_in, ROUTER_ADDRESS, amt * swap_fraction)
            tx = swap(web3, account, router, token_in, token_out, amt * swap_fraction)
            if tx: total_tx += 1
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
