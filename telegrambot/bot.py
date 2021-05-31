import logging
import datetime
from os import access

from telegram import Update, ForceReply, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN

from data_service import DataService


DIARYENTRY, MOOD, MOODVALUE, SEESTATS = range(4)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

mongodb_data_service = DataService(logger)

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Hi {user.mention_markdown_v2()}\! My name is Modia\. I am a bot\. I can track your mood and write a diary with you if you like\! Just say /hey or tap it and we can begin\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        "Don't know how to continue? Here is a list of commands you can use:\n (To be implemented)"
    )


def start_report(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "Hey :) Glad to hear from you! Tell me a bit about yesterday!"
    )

    return DIARYENTRY


def reset(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("I reset everything! You can have a fresh start :)")


def diary_entry(update: Update, _: CallbackContext) -> int:
    mongodb_data_service.insert_diary_entry(
        update.effective_user.id,
        update.message.text,
        datetime.datetime.now(datetime.timezone.utc),
    )
    update.message.reply_text(
        "I got you! How would you describe your mood yesterday? Just a few words are enough :)"
    )

    return MOOD


def mood(update: Update, _: CallbackContext) -> int:
    mongodb_data_service.insert_mood_description(
        update.effective_user.id,
        update.message.text,
        datetime.datetime.now(datetime.timezone.utc),
    )

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1"),
            InlineKeyboardButton("2", callback_data="2"),
            InlineKeyboardButton("3", callback_data="3"),
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("5", callback_data="5"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Got it! Now just rate your mood from 1 (very bad) to 5 (very good) for me :)",
        reply_markup=reply_markup,
    )

    return MOODVALUE


def mood_value(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="1"),
            InlineKeyboardButton("No", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        "Great! Do you want me to show your stats?", reply_markup=reply_markup
    )

    logger.info(query.data)

    mongodb_data_service.insert_mood_value(
        update.effective_user.id,
        query.data,
        datetime.datetime.now(datetime.timezone.utc),
    )

    return SEESTATS


def see_stats(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    access_token = mongodb_data_service.insert_new_access_token(
        update.effective_user.id
    )

    query.edit_message_text(
        "Okay, I wrote down your mood rating :) You can see your stats at https://notimplemented.com/stats?token="
        + access_token
        + " . This link will be working for the next 48 hours."
    )

    logger.info(query.data)

    return ConversationHandler.END


def stats(update: Update, _: CallbackContext) -> None:
    mongodb_data_service.get_mood_values(update.effective_user.id)
    update.message.reply_text("We are currently implementing stats...")


def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        "Okay we will stop here :) You can start again at any time with /hey!"
    )

    return ConversationHandler.END


def main() -> None:
    """Start the bot."""

    # Create database connection
    mongodb_data_service.connect()

    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("reset", reset))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("hey", start_report)],
        states={
            DIARYENTRY: [MessageHandler(Filters.text & ~Filters.command, diary_entry)],
            MOOD: [MessageHandler(Filters.text & ~Filters.command, mood)],
            MOODVALUE: [CallbackQueryHandler(mood_value, pattern="^[1-5]$")],
            SEESTATS: [CallbackQueryHandler(see_stats, pattern="^[1-2]$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
