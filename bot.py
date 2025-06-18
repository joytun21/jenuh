import json
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# === Load Konfigurasi dari .vars.json ===
with open("/root/BotVPN/.vars.json") as f:
    config = json.load(f)

BOT_TOKEN = config.get("BOT_TOKEN")
ADMIN_ID = int(config.get("USER_ID"))
GROUP_ID = int(config.get("GROUP_ID"))
NAMA_STORE = config.get("NAMA_STORE")

# === Logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Handler start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hai {user.first_name}!\n"
        f"Selamat datang di *{NAMA_STORE}*!\n\n"
        "Gunakan tombol di bawah ini untuk melihat menu:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📋 Menu", callback_data="menu")]]
        )
    )

# === Handler tombol menu ===
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📋 *Menu Utama:*\n\n"
        "1. 🔐 Trial Akun VPN\n"
        "2. 🛒 Beli Akun Premium\n"
        "3. ♻️ Perpanjang Akun\n"
        "4. 💳 Topup Saldo\n",
        parse_mode="Markdown"
    )

# === Main ===
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(menu_handler, pattern="^menu$"))

    app.run_polling()

if __name__ == "__main__":
    main()