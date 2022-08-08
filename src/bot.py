#! /usr/bin/python3.8


from os import remove, path, getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)
from dbusers import db_users
from dotenv import load_dotenv

import re
import logging

import messages
import converter
import send_email



# Global variable to store the user id and ebook file name in memory
state = {}

# Initiate DB
db = db_users()

# Credentials
load_dotenv()

ADMIN_ID = int(getenv('ADMIN_ID'))
ENV = getenv('ENV')

if ENV == "prod":
    TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
else:
    TELEGRAM_TOKEN = getenv('TEST_TELEGRAM_TOKEN')
    
EMAIL_SENDER = getenv('EMAIL_SENDER')
EMAIL_PASSWORD = getenv('EMAIL_PASSWORD')

# TODO
BANNED_USERS = []

# Bytes in 1MB
MB_IN_BYTES = 1048576

# File formats allowed
input_format = [
    ".azw",
    ".azw3",
    ".azw4",
    ".cbz",
    ".cbr",
    ".cbc",
    ".chm",
    ".djvu",
    ".docx",
    ".epub",
    ".fb2",
    ".fbz",
    ".html",
    ".htmlz",
    ".lit",
    ".lrf",
    ".mobi",
    ".odt",
    ".pdf",
    ".prc",
    ".pdb",
    ".pml",
    ".rb",
    ".rtf",
    ".snb",
    ".tcr",
    ".txt",
    ".txtz",
]
output_format = [
    ".azw3",
    ".epub",
    ".docx",
    ".fb2",
    ".htmlz",
    ".oeb",
    ".lit",
    ".lrf",
    ".mobi",
    ".pdb",
    ".pmlz",
    ".rb",
    ".pdf",
    ".rtf",
    ".snb",
    ".tcr",
    ".txt",
    ".txtz",
    ".zip",
]

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)
fh = logging.FileHandler("log.log")
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def clean_ebooks(file):
    """Remove file if file exist"""
    if path.isfile(file):
        remove(file)


def valid_email(email):
    """Check if email is valid"""
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def start(update: Update, context: CallbackContext) -> None:
    """When a user starts the bot, send help message and save its Telegram ID in DB"""
    help_command(update, context)
    user_id = update.message.chat.id
    logger.info(str(user_id) + " started the bot")
    db.add_item(user_id, "")


def delete_command(update: Update, context: CallbackContext) -> None:
    """Delete user from DB"""
    user_id = update.message.chat.id
    db.delete_item(user_id)
    update.message.reply_text(
        "✅ Your email and user ID have been deleted from the database."
    )


def email_command(update: Update, context: CallbackContext) -> None:
    """Check if email exists"""
    user_id = update.message.chat.id

    try:
        email = db.get_email(user_id)
        update.message.reply_text(messages.get_email(email))
    except:
        update.message.reply_text("ℹ️ Your email is not in the database")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued"""
    update.message.reply_html(messages.help())


def text_update(update: Update, context: CallbackContext) -> None:

    user_id = update.message.chat.id
    text_received = update.message.text.lower()

    if "@kindle.com" in text_received:
        if valid_email(text_received):
            try:
                db.add_item(user_id, text_received)
                logger.info(f"{user_id} saved email address")
                update.message.reply_html(messages.save_email(text_received))
            except Exception as e:
                logger.error(f"Error adding email to database {str(e)}")
                update.message.reply_text(
                    "❌ Error adding email to database. Try again")
        else:
            update.message.reply_text("That is not a valid email address")


def download_send(update: Update, context: CallbackContext) -> None:
    user_id = update.message.chat.id
    print(user_id)
    if user_id in BANNED_USERS:
        update.message.reply_text(
            "🚫 You have been banned for abusing the service"
        )
        return

    file = update.message.document.file_name
    _, file_extension = path.splitext(file)
    logger.info(str(user_id) + " send file: " + file_extension)
    file_id = update.message.document.file_id
    file_size = update.message.document.file_size / MB_IN_BYTES

    max_size_MB = 20
    if file_size <= max_size_MB:
        if file_extension.lower() in input_format:
            state[user_id] = [file, file_id]
            menu_donwload = [
                [InlineKeyboardButton("Send to Kindle", callback_data="send")],
                [
                    InlineKeyboardButton("EPUB", callback_data=".epub"),
                    InlineKeyboardButton("MOBI", callback_data=".mobi"),
                    InlineKeyboardButton("TXT", callback_data=".txt"),
                ],
                [
                    InlineKeyboardButton("AZW3", callback_data=".azw3"),
                    InlineKeyboardButton("DOCX", callback_data=".docx"),
                    InlineKeyboardButton("PDF", callback_data=".pdf"),
                ],
                [
                    InlineKeyboardButton("FB2", callback_data=".fb2"),
                    InlineKeyboardButton("LRF", callback_data=".lrf"),
                    InlineKeyboardButton("RTF", callback_data=".rtf"),
                ],
            ]
            reply_markup = InlineKeyboardMarkup(menu_donwload)
            update.message.reply_text(
                "Send to Kindle or Convert & Download:", reply_markup=reply_markup
            )
        else:
            context.bot.send_message(
                chat_id=user_id,
                text=messages.file_extension_not_valid(),
            )
            logger.info("Extension not valid: " + file_extension)
    else:
        context.bot.send_message(
            chat_id=user_id, text="❌ Error uploading file. Limit size is 20MB"
        )
        logger.info(str(user_id) + " send bigger file of " +
                    str(file_size) + " MB")


# all other menus
def menu_actions(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    if query.data == "send":
        # send to kindle
        selection = "send"
        extension_output = ".mobi"
        downloader(update, context, selection, extension_output)
    elif query.data in output_format:
        # convert and download
        selection = "download"
        extension_output = query.data
        downloader(update, context, selection, extension_output)


def downloader(update: Update, context: CallbackContext, selection, extension_output) -> None:

    user_id = update.effective_chat.id
    file, file_id = state.get(user_id)
    db.add_item(user_id, "")
    try:
        email = db.get_email(user_id)
    except:
        email = ""
    if email == "" and selection == "send":
        context.bot.send_message(
            chat_id=user_id,
            text=messages.update_email(),
            parse_mode="html",
        )
    else:

        file_name, file_extension = path.splitext(file)
        orig_file_path = "ebook/" + file_name + file_extension
        conv_file_path = "ebook/converted/" + file_name + extension_output

        try:
            context.bot.get_file(file_id).download(orig_file_path)
        except Exception as e:
            logger.error(str(e))
            context.bot.send_message(
                chat_id=user_id, text="❌ Error downloading the file. Try again."
            )
            clean_ebooks(orig_file_path)
            return
        if file_extension.lower() == ".mobi" and selection == "send":
            send_mail(context, user_id, email, file_name, orig_file_path)
        else:
            context.bot.send_message(
                chat_id=user_id, text='🛠️ Converting eBook "' + file_name + '". Please wait...'
            )
            try:
                logger.info(
                    str(user_id)
                    + " convert eBook "
                    + file_extension
                    + " -> "
                    + extension_output
                )
                converter.convert(extension_output)

            except Exception as e:
                context.bot.send_message(
                    chat_id=user_id,
                    text="❌ Error during conversion. Maybe your eBook is DRM locked. Try with another eBook",
                )
                logger.error(
                    "Error converting eBook "
                    + file_extension
                    + " to "
                    + extension_output
                )
                logger.error("Error conversion: " + str(e))
                clean_ebooks(conv_file_path)
                clean_ebooks(orig_file_path)
                return
            if selection == "send":
                send_mail(context, user_id, email, file_name, conv_file_path)
            else:
                try:
                    context.bot.send_document(
                        chat_id=user_id, document=open(conv_file_path, "rb"))
                    logger.info(str(user_id) + " eBook downloaded")
                except Exception as e:
                    logger.error("Error sending eBook: " + str(e))
                    context.bot.send_message(
                        chat_id=user_id, text="❌ Error sending the eBook. Please, try again.",)

        clean_ebooks(conv_file_path)
        clean_ebooks(orig_file_path)


def send_mail(context, user_id, recipient_email, file_name, attach_file_path):
    try:
        send_email.send_email(
            EMAIL_SENDER,
            EMAIL_PASSWORD,
            recipient_email,
            "Kindle Calibre Bot",
            "",
            attach_file_path,
        )
        context.bot.send_message(
            chat_id=user_id, text='🚀 "' + file_name + '" sent to ' + recipient_email
        )
        logger.info("Email sent to " + str(user_id))
    except Exception as e:
        logger.error("Error sending email: " + str(e))
        context.bot.send_message(
            chat_id=user_id,
            text="❌ Error sending the email to "
            + recipient_email
            + ". Check your email and try again.",
        )


def send_log(update: Update, context: CallbackContext):

    user_id = update.effective_chat.id
    if user_id == ADMIN_ID:
        context.bot.send_document(
            chat_id=ADMIN_ID, document=open("log.log", "rb"))


def main():
    """Start database."""
    db.setup()

    """Start the bot."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("delete", delete_command))
    dispatcher.add_handler(CommandHandler("email", email_command))
    dispatcher.add_handler(CommandHandler("log", send_log))

    # on noncommand
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, text_update))
    dispatcher.add_handler(CallbackQueryHandler(menu_actions))

    # on file
    updater.dispatcher.add_handler(
        MessageHandler(Filters.document, download_send))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
