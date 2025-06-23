import time
import random
from web3 import Web3
from eth_account import Account
from core.config import RPC_URL, ROUTER_ADDRESS, ROUTER_ABI, GTE_TOKENS
from core.utils.utils import print_header, show_balances, get_token_balance
from core.swap.swap import swap
from approve import approve_if_needed


def load_wallets():
    with open("private_keys.txt", "r") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    print_header()
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    router = web3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)
    private_keys = load_wallets()

    try:
        rounds = int(input("🔁 Berapa kali mau swap random per wallet? "))
        percent = float(input("💸 Berapa persen dari saldo token yang mau diswap tiap kali (contoh: 30)? "))
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

        total_tx = 0

        for i in range(rounds):
            print(f"\n🔁 SWAP RANDOM KE-{i + 1}")
            show_balances(web3, account)

            # Pilih token pair secara acak
            token_pair = random.sample(GTE_TOKENS, 2)
            token_in, token_out = token_pair[0], token_pair[1]

            if token_in == token_out:
                continue

            amt = get_token_balance(web3, account, token_in)
            if amt > 0:
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
