import os
import subprocess
from telethon import TelegramClient, events, Button

# Baca konfigurasi dari var.txt
def load_config():
    config = {}
    with open("kyt/var.txt", "r") as f:
        for line in f:
            if "=" in line:
                key, value = line.strip().split("=", 1)
                config[key] = value
    return config

config = load_config()

API_ID = 123456  # Ganti dengan API_ID Telegram kamu
API_HASH = "your_api_hash"  # Ganti dengan API_HASH Telegram kamu
BOT_TOKEN = config["BOT_TOKEN"]
ADMIN_ID = int(config["ADMIN"])
NAMA_TOKO = config["NAMA_TOKO"]

bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if event.sender_id != ADMIN_ID:
        await event.respond("❌ Kamu tidak punya izin untuk menggunakan bot ini.")
        return

    await event.respond(
        f"👋 Selamat datang di bot {NAMA_TOKO}!\nGunakan menu di bawah:",
        buttons=[
            [Button.inline("💻 Order SSH", data="order_ssh")],
        ]
    )


@bot.on(events.CallbackQuery(data=b"order_ssh"))
async def menu_order_ssh(event):
    await event.edit(
        "💻 *Menu SSH:*\nSilakan pilih layanan SSH yang tersedia.",
        buttons=[
            [Button.inline("🆕 Create", data="ssh_create"),
             Button.inline("🧪 Trial", data="ssh_trial")],
            [Button.inline("🗑️ Delete", data="ssh_delete")],
            [Button.inline("🔙 Kembali", data="back_menu")]
        ],
        parse_mode="markdown"
    )


@bot.on(events.CallbackQuery(data=b"back_menu"))
async def back_menu(event):
    await event.edit(
        f"👋 Selamat datang kembali di bot {NAMA_TOKO}!",
        buttons=[
            [Button.inline("💻 Order SSH", data="order_ssh")],
        ]
    )


def run_script(script_path):
    try:
        result = subprocess.check_output(["bash", script_path], stderr=subprocess.STDOUT)
        return result.decode()
    except subprocess.CalledProcessError as e:
        return f"❌ Error: {e.output.decode()}"


@bot.on(events.CallbackQuery(data=b"ssh_create"))
async def ssh_create(event):
    await event.answer("Membuat akun SSH...")
    output = run_script("kyt/scripts/create-ssh.sh")
    await event.respond(f"✅ *Akun SSH berhasil dibuat:*\n\n`{output}`", parse_mode="markdown")


@bot.on(events.CallbackQuery(data=b"ssh_trial"))
async def ssh_trial(event):
    await event.answer("Membuat akun trial SSH...")
    output = run_script("kyt/scripts/trial-ssh.sh")
    await event.respond(f"✅ *Trial SSH berhasil dibuat:*\n\n`{output}`", parse_mode="markdown")


@bot.on(events.CallbackQuery(data=b"ssh_delete"))
async def ssh_delete(event):
    await event.answer("Menghapus akun SSH...")
    output = run_script("kyt/scripts/delete-ssh.sh")
    await event.respond(f"🗑️ *Akun SSH berhasil dihapus:*\n\n`{output}`", parse_mode="markdown")


print("🤖 Bot berjalan...")
bot.run_until_disconnected()
