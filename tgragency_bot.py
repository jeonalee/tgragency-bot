from server import app
from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
from threading import Thread

# === TOKEN BOT ===
BOT_TOKEN = "8018572981:AAGN1UhKAahkRQ9RYLQcuV7pSsqh2iNIZdw"

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# === INLINE BUTTON (SUSUNAN SESUAI PERMINTAAN) ===
def rules_keyboard():
    keyboard = [
        [InlineKeyboardButton("PERATURAN GRUP", url="https://t.me/c/3205329878/382")],
        [
            InlineKeyboardButton("SEPUTAR\nCAPCUT", url="https://t.me/c/3205329878/383"),
            InlineKeyboardButton("CAPCUT BUDDY\n& PARTNER", url="https://t.me/c/3205329878/384")
        ],
        [
            InlineKeyboardButton("TEMPLATE DOMESTIK\n& NON-DOMESTIK", url="https://t.me/c/3205329878/385"),
            InlineKeyboardButton("LIST GRUP\n& INSTAGRAM", url="https://t.me/c/3205329878/386")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# === TEKS SAMBUTAN ===
def welcome_text(member):
    if member.username:
        mention = f"<a href='https://t.me/{member.username}'>@{member.username}</a>"
    else:
        mention = f"<a href='tg://user?id={member.id}'>{member.first_name}</a>"

    text = (
        f"<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗔𝗕𝗢𝗔𝗥𝗗! 🎉 {mention}</b>\n"
        f"<b>Selamat bergabung di TGR Agency! Ikuti panduan dan tunjukkan karya terbaikmu di sini! 🚀</b>"
    )
    return text

# === AUTO WELCOME MEMBER ===
def welcome_member(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        text = welcome_text(member)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=rules_keyboard()
        )

# === PERINTAH /RULES (HANYA ADMIN) ===
def rules_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_admins = context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in chat_admins]

    if user_id not in admin_ids:
        return  # Non-admin: bot diam saja

    text = (
        "<b>📘 Daftar Rules TGR Agency</b>\n"
        "Klik tombol di bawah untuk melihat setiap bagian panduan."
    )
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=rules_keyboard()
    )

# === KEEP ALIVE UNTUK REPLIT ===
def run_flask():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

# === MAIN FUNCTION ===
def main():
    keep_alive()

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_member))
    dp.add_handler(CommandHandler("rules", rules_command))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

