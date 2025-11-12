from telegram import Bot, Update, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

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
def welcome_text(member=None):
    if member and member.username:
        mention = f"[{member.first_name}](tg://user?id={member.id})"
        text = (
            f"<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗔𝗕𝗢𝗔𝗥𝗗! 🎉 {mention}</b>\n"
            f"<b>Selamat bergabung di TGR Agency! Ikuti panduan dan tunjukkan karya terbaikmu di sini! 🚀</b>"
        )
    else:
        text = (
            "<b>𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗔𝗕𝗢𝗔𝗥𝗗! 🎉</b>\n"
            "<b>Selamat bergabung di TGR Agency! Ikuti panduan dan tunjukkan karya terbaikmu di sini! 🚀</b>"
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

    text = welcome_text(None)
    context.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=rules_keyboard()
    )

# === PERINTAH /KICK (HANYA ADMIN) ===
def kick_member(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    chat_admins = context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in chat_admins]

    if user_id not in admin_ids:
        return  # Non-admin: tidak ada respon sama sekali

    # Jika /kick digunakan dengan reply
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        username = context.args[0].replace("@", "")
        try:
            member = context.bot.get_chat_member(chat_id, username)
            target = member.user
        except:
            update.message.reply_text("⚠️ Tidak dapat menemukan pengguna tersebut.")
            return
    else:
        update.message.reply_text("⚠️ Gunakan perintah /kick dengan membalas pesan anggota atau mention username.")
        return

    try:
        context.bot.kick_chat_member(chat_id, target.id)
        message = f"⚠️ <b>[{target.first_name}](tg://user?id={target.id})</b> telah dikeluarkan dari grup."
        context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
    except Exception as e:
        logging.error(f"Gagal mengeluarkan anggota: {e}")
        update.message.reply_text("❌ Gagal mengeluarkan anggota.")

# === MAIN FUNCTION ===
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome_member))
    dp.add_handler(CommandHandler("rules", rules_command))
    dp.add_handler(CommandHandler("kick", kick_member, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
