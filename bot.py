import json
import subprocess
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# ========== Load Konfigurasi ==========
with open(".vars.json", "r") as config_file:
    config = json.load(config_file)

BOT_TOKEN = config["BOT_TOKEN"]
ADMIN_ID = int(config["USER_ID"])
GROUP_ID = int(config["GROUP_ID"])
STORE_NAME = config["NAMA_STORE"]

# ========== /start Command ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Kamu tidak punya akses ke bot ini.")
        return

    keyboard = [
        [InlineKeyboardButton("🔒 SSH", callback_data="ssh")],
        [InlineKeyboardButton("⚡ VMESS", callback_data="vmess")],
        [InlineKeyboardButton("💠 VLESS", callback_data="vless")],
        [InlineKeyboardButton("🛡 TROJAN", callback_data="trojan")],
        [InlineKeyboardButton("💸 ISI SALDO", callback_data="saldo")]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"📡 Selamat datang di *{STORE_NAME}*\nSilakan pilih layanan:",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ========== Handle Button Click ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.edit_message_text("❌ Kamu tidak punya akses ke bot ini.")
        return

    pilihan = query.data
    script_map = {
        "ssh": "bash scripts/ssh.sh",
        "vmess": "bash scripts/vmess.sh",
        "vless": "bash scripts/vless.sh",
        "trojan": "bash scripts/trojan.sh",
        "saldo": "bash scripts/saldo.sh"
    }

    perintah = script_map.get(pilihan)
    if perintah:
        try:
            hasil = subprocess.check_output(perintah, shell=True, text=True)
            await query.edit_message_text(f"✅ Output dari *{pilihan.upper()}*:\n\n```\n{hasil}\n```", parse_mode="Markdown")
        except subprocess.CalledProcessError as e:
            await query.edit_message_text(f"❌ Gagal menjalankan script {pilihan}.\n{e}")
    else:
        await query.edit_message_text("❌ Layanan tidak dikenal.")

# ========== Main ==========
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot VPN aktif!")
    app.run_polling()