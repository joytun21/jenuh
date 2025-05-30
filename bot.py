import asyncio
from telethon import TelegramClient, events, Button
import os

# Fungsi baca konfigurasi dari var.txt
def load_config():
    config = {}
    with open("kyt/var.txt") as f:
        for line in f:
            if "=" in line:
                key, val = line.strip().split("=", 1)
                config[key.strip()] = val.strip().strip('"')
    return config

# Load config
config = load_config()
BOT_TOKEN = config.get("BOT_TOKEN")
ADMIN_ID = int(config.get("ADMIN", 0))
MERCHANT_ID = config.get("MERCHANT_ID")
API_KEY = config.get("API_KEY")
DATA_QRIS = config.get("DATA_QRIS")
NAMA_TOKO = config.get("NAMA_TOKO")

# API ID & HASH dummy (wajib diganti jika tidak pakai bot token-only mode)
API_ID = 123456
API_HASH = "0123456789abcdef0123456789abcdef"

# Inisialisasi bot Telethon
bot = TelegramClient("kytbot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Cek apakah user adalah admin
def is_admin(user_id):
    return user_id == ADMIN_ID

# /start command
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if not is_admin(event.sender_id):
        await event.reply("❌ Kamu tidak diizinkan menggunakan bot ini.")
        return
    await event.reply(f"""
📦 Bot Aktif!
👤 Admin: `{ADMIN_ID}`
🏪 Toko: *{NAMA_TOKO}*

Gunakan perintah:
/order_ssh - Order layanan SSH
""", parse_mode="markdown")

# /order_ssh menu
@bot.on(events.NewMessage(pattern="/order_ssh"))
async def order_ssh(event):
    if not is_admin(event.sender_id):
        await event.reply("❌ Kamu bukan admin.")
        return

    await event.respond(
        "📦 Pilih jenis layanan SSH:",
        buttons=[
            [Button.inline("🎁 Trial SSH", data="trial_ssh"), Button.inline("➕ Buat SSH", data="create_ssh")],
            [Button.inline("🔁 Perpanjang SSH", data="renew_ssh"), Button.inline("❌ Hapus SSH", data="delete_ssh")]
        ]
    )

# Handle tombol inline
@bot.on(events.CallbackQuery)
async def callback(event):
    data = event.data.decode()
    user_id = event.sender_id

    if not is_admin(user_id):
        await event.answer("❌ Kamu bukan admin.")
        return

    script_map = {
        "trial_ssh": "kyt/scripts/trialssh",
        "create_ssh": "kyt/scripts/addssh",
        "renew_ssh": "kyt/scripts/renewssh",
        "delete_ssh": "kyt/scripts/deletessh"
    }

    if data in script_map:
        script_path = script_map[data]
        await event.edit(f"🔄 Menjalankan `{data}` ...", parse_mode="markdown")
        os.system(f"bash {script_path}")
    else:
        await event.answer("❓ Aksi tidak dikenal.")

# Jalankan bot
print("🤖 Bot aktif dan menunggu perintah...")
bot.run_until_disconnected()
