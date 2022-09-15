#! /usr/bin/python3.8

from os import remove, path, getenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackContext,
    CallbackQueryHandler,
    filters,
)
import subprocess
from db import db_users
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

ADMIN_ID = int(getenv("ADMIN_ID"))
ENV = getenv("ENV")

if ENV == "prod":
    TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
else:
    TELEGRAM_TOKEN = getenv("TEST_TELEGRAM_TOKEN")

EMAIL_SENDER = getenv("EMAIL_SENDER")
EMAIL_PASSWORD = getenv("EMAIL_PASSWORD")

# Bytes in 1MB
MB_IN_BYTES = 1048576

# Max file size in megabytes
MAX_SIZE_MB = 20

# eBook file folder
EBOOK_FOLDER = "ebook/"

# Kindle file extension
KINDLE_EXTENSION = ".mobi"

# Daily conversion limit per user
DAILY_CONVERSION_LIMIT = 10

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
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


def clean_ebooks(file):
    # Remove file if file exist
    if path.isfile(file):
        remove(file)


def validate_email(email):
    # Check if email is valid
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # When a user starts the bot, send help message and save its Telegram ID in DB
    await help_command(update, context)
    user_id = update.message.chat.id
    logger.info(f"{str(user_id)} started the bot")
    try:
        db.add_user(user_id)
    except Exception as e:
        logger.error(f"Error adding user: {str(e)}")


async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Delete email from DB
    user_id = update.message.chat.id
    try:
        db.delete_email(user_id)
        await update.message.reply_text(
            "✅ Your email has been deleted from the database."
        )
    except Exception as e:
        logger.error(f"Error deleting email: {str(e)}")
        await update.message.reply_text("❌ Error deleting email from the database.")


async def email_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if email exists in DB and send email
    user_id = update.message.chat.id

    try:
        email = db.get_email(user_id)
        if email == "":
            await update.message.reply_text("ℹ️ Your email is not in the database")
            return
        await update.message.reply_text(messages.get_email(email))
    except:
        await update.message.reply_text("ℹ️ Your email is not in the database")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send help message when the command /help is issued
    await update.message.reply_html(messages.help())


async def update_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    user_id = update.message.chat.id
    text_received = update.message.text.lower()

    if "@kindle.com" not in text_received or not validate_email(text_received):
        await update.message.reply_text(
            "❌ That is not a valid email address. It should be xxx@kindle.com"
        )
        return

    try:
        db.update_email(user_id, text_received)
        logger.info(f"{user_id} saved email address")
        await update.message.reply_html(messages.save_email(text_received))
    except Exception as e:
        logger.error(f"Error adding email to database: {str(e)}")
        await update.message.reply_text("❌ Error adding email to database. Try again")


async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat.id

    file = update.message.document.file_name
    _, extension_input = path.splitext(file)
    file_id = update.message.document.file_id
    file_size = update.message.document.file_size / MB_IN_BYTES

    logger.info(f"{str(user_id)} send file: {extension_input}")

    if file_size > MAX_SIZE_MB:
        # Check if file is too big
        await context.bot.send_message(
            chat_id=user_id, text="❌ Error uploading file. Limit size is 20MB"
        )
        logger.info(f"{str(user_id)} send file of {str(file_size)}MB. Limit exceeded")
        return

    if extension_input.lower() not in input_format:
        # Check if file is valid
        await context.bot.send_message(
            chat_id=user_id,
            text=messages.file_extension_not_valid(),
        )
        logger.info(f"Extension not valid: {extension_input}")
        return

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
    await update.message.reply_text(
        "Send to Kindle or Convert & Download:", reply_markup=reply_markup
    )


async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.data == "send":
        # send to kindle
        selection = "send"
        extension_output = KINDLE_EXTENSION
    elif query.data in output_format:
        # convert and download
        selection = "download"
        extension_output = query.data

    await process_file(update, context, selection, extension_output)


async def process_file(
    update: Update, context: CallbackContext, selection, extension_output
) -> None:

    user_id = update.effective_chat.id

    try:
        db.add_user(user_id)

        if db.is_banned(user_id) and user_id != ADMIN_ID:
            await context.bot.send_message(
                chat_id=user_id,
                text="🚫 You have been temporary banned for abusing the service",
            )
            return

        if (
            db.get_user_downloads_today(user_id) >= DAILY_CONVERSION_LIMIT
            and user_id != ADMIN_ID
        ):
            await context.bot.send_message(
                chat_id=user_id,
                text=f"🚫 You have reached the maximum number of conversions for today ({DAILY_CONVERSION_LIMIT}). Try again tomorrow",
            )
            await context.bot.send_message(
                chat_id=user_id,
                text="ℹ️ This limit has been applied to avoid abuse of the service that would prevent proper operation for other users",
            )
            return

    except Exception as e:
        logger.error(f"Error reading database: {str(e)}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Error reading database. Try again",
        )
        return

    try:
        file, file_id = state.get(user_id)
    except Exception as e:
        # This error usually means that bot has been restarted
        # and the state has been lost
        logger.error(f"Error reading global dictionary): {str(e)}")
        await context.bot.send_message(
            chat_id=user_id,
            text="❌ Internal error. Please, send the file again",
        )
        return

    file_name, extension_input = path.splitext(file)
    orig_file_path = f"{EBOOK_FOLDER}{file_name}{extension_input}"
    conv_file_path = f"{EBOOK_FOLDER}{file_name}{extension_output}"

    # Get user email
    try:
        email = db.get_email(user_id)
    except:
        email = ""

    if email == "" and selection == "send":
        # Email not found and user want to send to kindle
        await context.bot.send_message(
            chat_id=user_id,
            text=messages.update_email(),
            parse_mode="html",
        )
        return

    if selection == "download" and extension_input == extension_output:
        # No need to convert, same extension
        await context.bot.send_message(
            chat_id=user_id,
            text=f"ℹ️ eBook already in the selected format ({extension_output})",
            parse_mode="html",
        )
        return

    try:
        # Download file
        down_file = await context.bot.get_file(file_id)
        await down_file.download(
            orig_file_path,
        )
    except Exception as e:
        logger.error(f"Error downloading the file: {str(e)}")
        await context.bot.send_message(
            chat_id=user_id, text="❌ Error downloading the file. Try again."
        )
        clean_ebooks(orig_file_path)
        return

    if extension_input.lower() == KINDLE_EXTENSION and selection == "send":
        # No conversion needed, just send to kindle
        send_mail(context, user_id, email, file_name, orig_file_path, extension_input)

    else:
        # The file must be converted
        await context.bot.send_message(
            chat_id=user_id,
            text=messages.conversion(file_name, extension_input, extension_output),
        )
        logger.info(
            f"{str(user_id)} converting {extension_input} to {extension_output}"
        )

        try:
            converter.convert(extension_output, orig_file_path, conv_file_path)
        except subprocess.TimeoutExpired:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Conversion timeout. Try again or send another file",
            )
            logger.error(
                f"Conversion timeout from {extension_input} to {extension_output}"
            )
            clean_ebooks(orig_file_path)
            clean_ebooks(orig_file_path)
            return

        except Exception as e:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Error during conversion. Maybe your eBook is DRM locked. Try with another eBook",
            )
            logger.error(
                f"Error during conversion from {extension_input} to {extension_output}: {str(e)}"
            )

            clean_ebooks(conv_file_path)
            clean_ebooks(orig_file_path)
            return

        if selection == "send":
            # Send to kindle
            send_mail(
                context, user_id, email, file_name, conv_file_path, extension_input
            )
        else:
            # Send converted file to telegram
            try:

                await context.bot.send_document(
                    chat_id=user_id,
                    document=open(conv_file_path, "rb"),
                )
                db.add_download(user_id, extension_input, extension_output, False)
                logger.info(f"{str(user_id)} eBook downloaded")

            except Exception as e:
                logger.error("Error sending eBook: " + str(e))
                await context.bot.send_message(
                    chat_id=user_id,
                    text="❌ Error sending the eBook. Please, try again.",
                )

    clean_ebooks(conv_file_path)
    clean_ebooks(orig_file_path)


async def send_mail(
    context, user_id, recipient_email, file_name, attach_file_path, extension_input
):

    try:
        send_email.send_email(
            EMAIL_SENDER,
            EMAIL_PASSWORD,
            recipient_email,
            "Kindle Calibre Bot",
            "",
            attach_file_path,
        )
        await context.bot.send_message(
            chat_id=user_id, text=f'🚀 "{file_name}" sent to {recipient_email}'
        )
        db.add_download(user_id, extension_input, KINDLE_EXTENSION, True)
        logger.info(f"Email sent to {str(user_id)}")

    except Exception as e:
        logger.error(f"Error sending the email: {str(e)}")
        await context.bot.send_message(
            chat_id=user_id,
            text=f"❌ Error sending the email to {recipient_email}. Please, check your email and try again.",
        )


async def send_message_to_all_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a message to all users in the database

    user_id = update.effective_chat.id

    if user_id != ADMIN_ID:
        return

    message = " ".join(context.args)

    if message == "" or message == " ":
        await update.message.reply_text("❌ You must specify a message")
        return

    try:
        users = db.get_all_users()
    except Exception as e:
        logger.error(f"Error getting all users from DB: {str(e)}")
        return

    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=message)
        except Exception as e:
            logger.error(f"Error sending broadcast message to {user[0]}: {str(e)}")

    await update.message.reply_text("✅ Message sent to all users")


async def send_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send the log file to admin user
    user_id = update.effective_chat.id

    if user_id != ADMIN_ID:
        return

    await context.bot.send_document(chat_id=ADMIN_ID, document=open("log.log", "rb"))


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send the top downloads to admin user
    user_id = update.effective_chat.id

    if user_id != ADMIN_ID:
        return

    try:
        top_user_downloads = db.get_top_users_downloads()
        monthly_user_downloads = db.get_top_users_monthly_downloads()
        total_downloads = db.get_total_downloads()
        monthly_downloads = db.get_monthly_downloads()
        downloads_by_month = db.get_downloads_by_month()
        total_users = db.get_total_users()

        await update.message.reply_text(f"ℹ️ Total downloads: {total_downloads}")
        await update.message.reply_text(
            f"ℹ️ Total downloads last 30 days: {monthly_downloads}"
        )
        await update.message.reply_text(
            f"ℹ️ Total users downloads [10]: {top_user_downloads}"
        )
        await update.message.reply_text(
            f"ℹ️ Monthly users downloads [10]: {monthly_user_downloads}"
        )
        await update.message.reply_text(f"ℹ️ Downloads by month: {downloads_by_month}")
        await update.message.reply_text(f"ℹ️ Total users: {total_users}")

    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        await update.message.reply_text("❌ Error getting stats.")


def main():
    # Start database
    db.setup()

    # Start the bot
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # on different commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("delete", delete_command))
    application.add_handler(CommandHandler("email", email_command))
    application.add_handler(CommandHandler("log", send_log))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("send", send_message_to_all_users))

    # on text message
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, update_email)
    )

    # on query selection
    application.add_handler(CallbackQueryHandler(select_action, block=False))

    # on file
    application.add_handler(MessageHandler(filters.ATTACHMENT, show_menu))

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()
