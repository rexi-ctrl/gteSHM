# GTE dan bronto Testnet Swap Bot

Bot ini dirancang untuk melakukan swap token secara otomatis di jaringan MegaETH Testnet (GTE) menggunakan berbagai DEX seperti Uniswap dan Bronto (FDEX). Bot ini mendukung multi-wallet dan melakukan wrapping ETH, approve, dan swap secara acak untuk token tertentu.

## 🚀 Fitur

- Swap otomatis antar dex BRONTO dan GTE
- Dukung multi-wallet (dari file `private_keys.txt`)
- Pilihan DEX: GTE, FDEX/BRONTO, atau random
- Support wrapping ETH ke WETH
- Auto-approve token sebelum swap
- Notifikasi hasil swap via Telegram
- Logging saldo, aktivitas swap, dan TX count

## 🧩 Struktur Folder

```
.
├── main.py               # Script utama bot
├── private_keys.txt      # File berisi private key (1 per baris)
├── .env                  # Konfigurasi token Telegram & pengaturan
├── core/
│   ├── config.py         # Berisi konfigurasi RPC dan ABI
│   ├── swap/swap.py      # Fungsi utama swap token
│   └── utils/utils.py    # Fungsi utilitas
├── approve.py            # Fungsi approve token
└── README.md             # Dokumentasi
```

## ⚙️ Instalasi

1. Clone repositori ini:
```bash
git clone https://github.com/namamu/gte-swap-bot.git
cd gte-swap-bot
```

2. Install dependency:
```bash
pip install -r requirements.txt
```

3. Buat file `.env`:
```env
TELEGRAM_BOT_TOKEN=xxxxxx
TELEGRAM_CHAT_ID=xxxxxx
DEX_OVERRIDE=auto  # Pilihan: uniswap, fdex, auto
```

4. Tambahkan private key ke file `private_keys.txt`:
```
0xabc123...
0xdef456...
```

## ▶️ Cara Menjalankan

Jalankan bot dengan:
```bash
python main.py --dex auto
```
Opsi `--dex` bisa diisi:
- `uniswap`
- `fdex`
- `auto` (default, random per TX)

Bot akan menanyakan:
- Jumlah swap per wallet
- Persentase saldo token yang ingin diswap
- Jumlah ETH yang ingin di-wrap ke WETH

## 🧪 Catatan Penting
- Ini adalah bot untuk testnet (MegaETH).
- **Jangan gunakan untuk private key wallet utama.**
- Pastikan wallet punya ETH testnet cukup untuk gas.
- Waktu antar wallet dibuat random untuk menghindari pola.

📎X: [@belchman_](https://x.com/belchman_)

---

**Disclaimer:** Penggunaan script ini sepenuhnya tanggung jawab pengguna.
