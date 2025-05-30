from telethon import TelegramClient, events
import sqlite3, os

# Load konfigurasi
exec(open("kyt/var.txt").read())

# Inisialisasi bot
bot = TelegramClient("kytbot_session", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e").start(bot_token=BOT_TOKEN)

# Inisialisasi database jika belum ada
def init_db():
    if not os.path.exists("kyt/database.db"):
        conn = sqlite3.connect("kyt/database.db")
        cur = conn.cursor()
        cur.execute("CREATE TABLE admin (user_id INTEGER)")
        cur.execute("INSERT INTO admin (user_id) VALUES (?)", (ADMIN,))
        conn.commit()
        conn.close()

def is_admin(user_id):
    conn = sqlite3.connect("kyt/database.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM admin WHERE user_id = ?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if not is_admin(event.sender_id):
        await event.respond("🚫 Anda tidak memiliki akses.")
        return
    await event.respond(
        f"""
👋 Halo, Admin!

📍 Selamat datang di bot AutoOrder.
Silakan pilih menu:

/order_ssh - Order SSH
/order_vmess - Order VMess
/order_vless - Order VLess
/order_trojan - Order Trojan

💳 QRIS Payment: {NAMA_TOKO}
"""
    )
from kyt.handlers import order_ssh
init_db()
print("🤖 Bot sedang berjalan...")
bot.run_until_disconnected()
