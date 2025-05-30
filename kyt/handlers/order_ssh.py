from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes

# Fungsi saat user ketik /order_ssh
async def order_ssh_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Trial SSH", callback_data='ssh_trial')],
        [InlineKeyboardButton("🛠️ Buat SSH", callback_data='ssh_create')],
        [InlineKeyboardButton("♻️ Perpanjang SSH", callback_data='ssh_renew')],
        [InlineKeyboardButton("❌ Hapus SSH", callback_data='ssh_delete')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan pilih layanan SSH:", reply_markup=reply_markup)

# Handler tombol
async def ssh_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ssh_trial":
        await query.edit_message_text("🔧 Anda memilih *Trial SSH*. (Dalam pengembangan)", parse_mode="Markdown")
    elif data == "ssh_create":
        await query.edit_message_text("🛠️ Anda memilih *Buat SSH*. (Dalam pengembangan)", parse_mode="Markdown")
    elif data == "ssh_renew":
        await query.edit_message_text("♻️ Anda memilih *Perpanjang SSH*. (Dalam pengembangan)", parse_mode="Markdown")
    elif data == "ssh_delete":
        await query.edit_message_text("❌ Anda memilih *Hapus SSH*. (Dalam pengembangan)", parse_mode="Markdown")
    else:
        await query.edit_message_text("❓ Pilihan tidak dikenal.")

# Fungsi untuk ditambahkan ke bot
def get_handler():
    return [
        CommandHandler("order_ssh", order_ssh_menu),
        CallbackQueryHandler(ssh_callback_handler, pattern="^ssh_"),
    ]