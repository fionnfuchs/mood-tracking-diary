import logging
import datetime
import pytz
from os import access

from locale_strings import locale_strings

from message_utils import (
    validate_current_time,
    get_timezone_by_current_time,
    get_polltime_by_message_time,
)

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

DIARYENTRY, MOOD, MOODVALUE, SEESTATS, LANGUAGE, TIMEZONE_CURRENTTIME, REMINDER = range(
    7
)

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

    # New user? -> Ask to perform /setup (or start setup automatically?)
    update_daily_reminder(update)

    update.message.reply_text(
        locale_strings[user_dict[update.effective_user.id]["language"]]["greeting"],
        reply_markup=ForceReply(selective=True),
    )


def update_daily_reminder(update):
    if update.effective_user.id not in job_queue_user_list:
        logger.info("Adding job to notify user.")
        set_daily_reminder(job_queue, update.message.chat.id, update.effective_user.id)
    else:
        logger.info("Job already created for user. Skipping...")


def set_daily_reminder(job_queue, chatid, userid):
    polltime = user_dict[userid]["polltime"]
    timezone = user_dict[userid]["timezone"]
    if polltime != "undefined" and timezone != "undefined":
        t = datetime.time(hour=int(polltime), minute=00, tzinfo=pytz.timezone(timezone))
        job_queue.run_daily(start_report_auto, time=t, context=chatid)
        job_queue_user_list.append(userid)
        logger.info(
            "Set reminder at hour " + str(polltime) + " in timezone " + str(timezone)
        )
    else:
        logger.info(
            "No polltime and or timezone set. Not setting up daily reminder job."
        )


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        locale_strings[user_dict[update.effective_user.id]["language"]]["help"]
    )


def reset(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]]["reset"]
    )


# -----------
#   REPORT
# -----------


def start_report(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "start_report"
        ]
    )

    return DIARYENTRY


def start_report_auto(context: CallbackContext) -> int:
    context.bot.send_message(
        chat_id=context.job.context,
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "start_report_auto"
        ],
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


# -----------
#   SETUP
# -----------


def start_setup(update: Update, _: CallbackContext) -> int:

    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="1"),
            InlineKeyboardButton("German", callback_data="2"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "start_setup"
        ],
        reply_markup=reply_markup,
    )

    return LANGUAGE


def language(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    language = "en"

    if query.data == "2":
        language = "de"

    mongodb_data_service.set_user_language(update.effective_user.id, language)
    update_user_dict()

    # Languages 1 = EN, 2 = DE, query.data
    # User is asked for current time for timezone purposes

    query.edit_message_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "language_reply"
        ]
    )

    return TIMEZONE_CURRENTTIME


def timezone_currenttime(update: Update, _: CallbackContext) -> int:

    logger.info("Got current time: " + update.message.text)

    if not validate_current_time(update.message.text):

        update.message.reply_text(
            text=locale_strings[user_dict[update.effective_user.id]["language"]][
                "timezone_invalid_reply"
            ]
        )

        return TIMEZONE_CURRENTTIME

    timezone = get_timezone_by_current_time(update.message.text)
    mongodb_data_service.set_user_timezone(update.effective_user.id, timezone)
    update_user_dict()

    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "timezone_reply"
        ]
    )

    return REMINDER


def reminder(update: Update, _: CallbackContext) -> int:

    if not validate_current_time(update.message.text):

        update.message.reply_text(
            text=locale_strings[user_dict[update.effective_user.id]["language"]][
                "timezone_invalid_reply"
            ]
        )

        return TIMEZONE_CURRENTTIME

    polltime = get_polltime_by_message_time(update.message.text)
    mongodb_data_service.set_user_polltime(update.effective_user.id, polltime)
    logger.info("Got polltime hour " + str(polltime))

    update.message.reply_text(
        text=locale_strings[user_dict[update.effective_user.id]["language"]][
            "reminder_reply"
        ]
    )

    update_user_dict()
    update_daily_reminder(update)

    return ConversationHandler.END


def update_user_dict():
    global user_dict
    user_list = mongodb_data_service.get_all_users()
    for user in user_list:
        logger.info(user)
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
    conv_handler_report = ConversationHandler(
        entry_points=[CommandHandler("hey", start_report)],
        states={
            DIARYENTRY: [MessageHandler(Filters.text & ~Filters.command, diary_entry)],
            MOOD: [MessageHandler(Filters.text & ~Filters.command, mood)],
            MOODVALUE: [CallbackQueryHandler(mood_value, pattern="^[1-5]$")],
            SEESTATS: [CallbackQueryHandler(see_stats, pattern="^[1-2]$")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    conv_handler_setup = ConversationHandler(
        entry_points=[CommandHandler("setup", start_setup)],
        states={
            LANGUAGE: [CallbackQueryHandler(language, pattern="^[1-2]$")],
            TIMEZONE_CURRENTTIME: [
                MessageHandler(Filters.text & ~Filters.command, timezone_currenttime)
            ],
            REMINDER: [MessageHandler(Filters.text & ~Filters.command, reminder)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler_report)
    dispatcher.add_handler(conv_handler_setup)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
