import logging
import datetime
import pytz
from os import access

from locale_strings import locale_strings

from telegram import (
    Update,
    ForceReply,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)
from telegram.ext.jobqueue import JobQueue

from config import BOT_TOKEN

from data_service import DataService

DIARYENTRY, MOOD, MOODVALUE, SEESTATS = range(4)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

mongodb_data_service = DataService(logger)
job_queue = None
job_queue_user_list = []
user_dict = {}

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _) -> None:
    """Executed on /start command. Setup some data and notification jobs for the user if it does not exist already."""
    user = update.effective_user

    if not mongodb_data_service.user_exists(user.id):
        mongodb_data_service.insert_user_object(user.id, update.message.chat.id)
        update_user_dict()
    else:
        logger.info("This user already exists. Not creating a new user object...")

    if update.effective_user.id not in job_queue_user_list:
        logger.info("Adding job to notify user.")
        set_daily_reminder(job_queue, update.message.chat.id)
        job_queue_user_list.append(update.effective_user.id)
    else:
        logger.info("Job already created for user. Skipping...")

    update.message.reply_text(
        locale_strings[user_dict[update.effective_user.id]["language"]]["greeting"],
        reply_markup=ForceReply(selective=True),
    )


def set_daily_reminder(job_queue, chatid):
    t = datetime.time(hour=21, minute=00, tzinfo=pytz.timezone("Europe/Berlin"))
    job_queue.run_daily(start_report_auto, time=t, context=chatid)


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        locale_strings[user_dict[update.effective_user.id]["language"]]["help"]
    )


def start_report_auto(context: CallbackContext) -> int:
    context.bot.send_message(
        chat_id=context.job.context,
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "start_report_auto"
        ],
    )


def start_report(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "start_report"
        ]
    )

    return DIARYENTRY


def reset(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]]["reset"]
    )


def diary_entry(update: Update, _: CallbackContext) -> int:
    mongodb_data_service.insert_diary_entry(
        update.effective_user.id,
        update.message.text,
        datetime.datetime.now(datetime.timezone.utc),
    )
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "diary_entry_reply"
        ]
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
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "mood_reply"
        ],
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

    mood_value_count = len(
        mongodb_data_service.get_mood_values(update.effective_user.id)
    )
    logger.info(mood_value_count)

    mongodb_data_service.insert_mood_value(
        update.effective_user.id,
        query.data,
        datetime.datetime.now(datetime.timezone.utc),
    )

    if mood_value_count >= 3:
        query.edit_message_text(
            text=locale_strings[user_dict[update.effective_user.id]["language"]][
                "mood_value_reply"
            ],
            reply_markup=reply_markup,
        )
    else:
        query.edit_message_text("Great!")
        return ConversationHandler.END
    return SEESTATS


def see_stats(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    if query.data == "1":
        access_token = mongodb_data_service.insert_new_access_token(
            update.effective_user.id
        )
        link = "https://notimplemented.com/stats?token=" + access_token
        query.edit_message_text(
            text=locale_strings[user_dict[update.effective_user.id]["language"]][
                "stats_link"
            ].replace("<link>", link)
        )
    else:
        query.edit_message_text(
            text=locale_strings[user_dict[update.effective_user.id]["language"]][
                "stats_nolink"
            ]
        )

    logger.info(query.data)

    return ConversationHandler.END


def stats(update: Update, _: CallbackContext) -> None:
    mongodb_data_service.get_mood_values(update.effective_user.id)
    update.message.reply_text("We are currently implementing stats...")


def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]]["cancel"],
    )

    return ConversationHandler.END


def update_user_dict():
    global user_dict
    user_list = mongodb_data_service.get_all_users()
    for user in user_list:
        user_dict[user["userid"]] = user


def main() -> None:
    """Start the bot."""
    global job_queue
    global mongodb_data_service

    # Create database connection
    mongodb_data_service.connect()
    update_user_dict()

    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)
    job_queue = updater.job_queue

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start, pass_job_queue=True))
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
