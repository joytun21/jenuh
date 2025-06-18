from telethon import TelegramClient, events, Button
import os
import json
import subprocess

# Load config
with open('/root/BotVPN/.vars.json') as f:
    config = json.load(f)

BOT_TOKEN = config['BOT_TOKEN']
ADMIN_ID = int(config['USER_ID'])
GROUP_ID = int(config['GROUP_ID']) if config['GROUP_ID'] else None
NAMA_STORE = config['NAMA_STORE']

# API ID dan HASH harus kamu ambil dari https://my.telegram.org
# Jika belum punya, buat di sana
API_ID = 1234567         # ganti sesuai API ID kamu
API_HASH = 'your_api_hash_here'

# Buat client
bot = TelegramClient('botvpn', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


def cek_akses(user_id):
    return user_id == ADMIN_ID


@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    sender = await event.get_sender()
    if not cek_akses(sender.id):
        await event.reply("🚫 Maaf, kamu tidak punya akses ke bot ini.")
        return
    
    await event.reply(f"👋 Halo admin {NAMA_STORE}, ketik /menu untuk lihat menu bot.")


@bot.on(events.NewMessage(pattern='/menu'))
async def menu_handler(event):
    sender = await event.get_sender()
    if not cek_akses(sender.id):
        await event.reply("🚫 Maaf, kamu tidak punya akses ke bot ini.")
        return

    inline_buttons = [
        [Button.inline(" SSH OVPN MANAGER ", b"ssh")],
        [Button.inline(" VMESS MANAGER ", b"vmess"),
         Button.inline(" VLESS MANAGER ", b"vless")],
        [Button.inline(" TROJAN MANAGER ", b"trojan"),
         Button.inline(" SHDWSK MANAGER ", b"shadowsocks")],
        [Button.inline(" CHECK VPS INFO ", b"info"),
         Button.inline(" OTHER SETTING ", b"setting")],
        [Button.inline(" ‹ Back Menu › ", b"start")]
    ]

    # Contoh data VPS info sederhana
    try:
        ssh_count = subprocess.check_output('grep "/home" /etc/passwd | grep -c "false"', shell=True).decode().strip()
        ip_vps = subprocess.check_output("curl -s ipv4.icanhazip.com", shell=True).decode().strip()
        os_name = subprocess.check_output("grep -w PRETTY_NAME /etc/os-release | head -1 | cut -d= -f2 | tr -d '\"'", shell=True).decode().strip()
    except Exception as e:
        ssh_count = "0"
        ip_vps = "Unknown"
        os_name = "Unknown"

    msg = f"""
━━━━━━━━━━━━━━━━━━━━━━━
⚡ ADMIN PANEL MENU ⚡
━━━━━━━━━━━━━━━━━━━━━━━
» OS     : {os_name}
» IP VPS : {ip_vps}
» Store  : {NAMA_STORE}

» Total SSH OVPN Accounts: {ssh_count}
━━━━━━━━━━━━━━━━━━━━━━━
    """
    await event.reply(msg, buttons=inline_buttons)


@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode('utf-8')
    sender = await event.get_sender()
    if not cek_akses(sender.id):
        await event.answer("🚫 Akses ditolak!", alert=True)
        return
    
    if data == 'ssh':
        await event.edit("🚀 Masuk ke SSH OVPN Manager...\n(implementasikan menu lebih lanjut)")
    elif data == 'vmess':
        await event.edit("🚀 Masuk ke VMESS Manager...\n(implementasikan menu lebih lanjut)")
    elif data == 'vless':
        await event.edit("🚀 Masuk ke VLESS Manager...\n(implementasikan menu lebih lanjut)")
    elif data == 'trojan':
        await event.edit("🚀 Masuk ke TROJAN Manager...\n(implementasikan menu lebih lanjut)")
    elif data == 'shadowsocks':
        await event.edit("🚀 Masuk ke SHADOWSOCKS Manager...\n(implementasikan menu lebih lanjut)")
    elif data == 'info':
        await event.edit("🔍 Info VPS:\n- OS: {os_name}\n- IP: {ip_vps}\n(implementasikan info lebih lengkap)")
    elif data == 'setting':
        await event.edit("⚙️ Setting lain-lain (implementasikan sesuai kebutuhan)")
    elif data == 'start':
        await event.edit("🏠 Kembali ke menu utama")
        await menu_handler(event)
    else:
        await event.answer("❌ Tombol tidak dikenali!", alert=True)


def main():
    print("Bot started...")
    bot.run_until_disconnected()


if __name__ == "__main__":
    main()