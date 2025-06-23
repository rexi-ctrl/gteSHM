
# 🔁 GTE Auto Swap Bot — Powered by SAHME

Bot Python untuk melakukan auto-swap token secara random di jaringan **GTE Testnet**.  
Sudah support multi-wallet, auto-wrap native ETH, auto-approve token, dan notifikasi ke Telegram.  
Cocok buat farming testnet, demo project, atau uji strategi swap massal.

---

## 🚀 Fitur Utama

- ✅ Auto swap antar token (GTE, USD, WETH)
- ✅ Support multi wallet (`private_keys.txt`)
- ✅ Delay antar wallet & transaksi
- ✅ Auto-approve token sebelum swap
- ✅ Auto-wrap native ETH ke WETH (dengan input jumlah)
- ✅ Input custom jumlah swap & loop
- ✅ Notifikasi sukses ke Telegram (Markdown styled)
- ✅ Tampilkan saldo token & native ETH

---

## 📁 Struktur File

```
.
├── main.py                  # Bot utama
├── approve.py              # Fungsi approve token
├── wrap_eth.py             # Fungsi auto-wrap ETH → WETH
├── notify.py               # Kirim notifikasi Telegram
├── private_keys.txt        # List private key (1 wallet per baris)
├── requirements.txt        # Daftar dependensi
├── .env                    # Konfigurasi Telegram bot
├── core/
│   ├── config.py           # Konfigurasi jaringan & token
│   ├── __init__.py
│   └── utils/
│       └── utils.py        # Show balances, headers, dll
│   └── swap/
│       └── swap.py         # Fungsi utama swap
```

---

## 🛠 Cara Pakai

1. Clone repo ini
2. Install dependensi:
   ```
   pip install -r requirements.txt
   ```
3. Siapkan `.env`:
   ```env
   TELEGRAM_BOT_TOKEN=token_kamu
   TELEGRAM_CHAT_ID=chat_id_kamu
   ```
4. Tambahkan wallet ke `private_keys.txt`
5. Jalankan bot:
   ```
   python main.py
   ```

---

## 📦 Contoh Output

```
👛 Wallet #1: 0x6E25...
💠 Saldo native ETH kamu: 0.0412
💠 Wrapping 0.0150 ETH to WETH...
🎯 Swap random: USD → GTE
✅ Swap berhasil: https://megascan.xyz/tx/0xabc...
📬 Notifikasi dikirim ke Telegram!
```

---

## 🤖 By SAHME
Buat kamu yang suka testnet, farming, & ngegas bot swap!  
Follow Sahme for more GTE-powered tools. ✊
