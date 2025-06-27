

def get_onchain_tx_count(web3, address):
    try:
        return web3.eth.get_transaction_count(address)
    except Exception as e:
        print(f"❌ Gagal ambil total TX onchain: {e}")
        return None

def main():
    print("==================================================")
    print("🔥 GTE AUTO SWAP BOT - Powered by SAHME 🔥")
    print("==================================================")

    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    router, router_address = get_rotated_router(web3)
    private_keys = load_wallets()
    WETH = Web3.to_checksum_address("0x776401b9bc8aae31a685731b7147d4445fd9fb19")
    gas_price_gwei = 0.1

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
        print(f"==================================================")
        print(f"👛 Wallet #{idx}: {account.address}")
        print(f"==================================================")

        native_eth = get_native_balance(web3, account)
        print(f"💠 Saldo native ETH kamu: {native_eth:.4f}")

        onchain_total = get_onchain_tx_count(web3, account.address)
        if onchain_total is not None:
            print(f"📦 Total TX on-chain: {onchain_total}")

        if native_eth > wrap_amount:
            wrap_eth(web3, account, WETH, wrap_amount, gas_price_gwei)

        print("🎉 Semua wallet selesai swap hari ini.")
        print("🤖 Bot by SAHME — GTE Testnet domination started.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("
⛔ Dibatalkan oleh user.")
