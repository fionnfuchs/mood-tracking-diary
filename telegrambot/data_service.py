import pymongo
import pytz
from tokens import create_secret_token
from datetime import datetime
from pytz import timezone


class DataService:
    def __init__(self, logger):
        self.client = None
        self.database = None
        self.logger = logger

    def connect(self):
        self.client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.database = self.client["userdata"]

    def insert_user_object(self, user, chatid):
        user_col = self.database["users"]
        new_user_object = {
            "userid": user,
            "chatid": chatid,
            "timezone": "undefined",
            "polltime": "undefined",
            "language": "de",
        }
        result = user_col.insert(new_user_object)
        self.logger.info(result)

    def set_user_timezone(self, user, timezone):
        user_col = self.database["users"]
        result = user_col.update({"userid": user}, {"$set": {"timezone": timezone}})
        self.logger.info(result)

    def set_user_language(self, user, language):
        user_col = self.database["users"]
        result = user_col.update({"userid": user}, {"$set": {"language": language}})
        self.logger.info(result)

    def set_user_polltime(self, user, polltime):
        user_col = self.database["users"]
        result = user_col.update({"userid": user}, {"$set": {"polltime": polltime}})
        self.logger.info(result)

    def get_all_users(self):
        user_col = self.database["users"]
        result_docs = user_col.find()
        result = []
        for user in result_docs:
            result.append(user)
        return result

    def user_exists(self, user):
        user_col = self.database["users"]
        query = {"userid": user}
        result_docs = user_col.find(query)
        for _ in result_docs:
            return True
        return False

    def insert_diary_entry(self, user, entry, timestamp):
        diary_col = self.database["diary_entries"]
        new_diary_entry = {"userid": user, "entry": entry, "timestamp": timestamp}
        result = diary_col.insert(new_diary_entry)
        self.logger.info(user)
        self.logger.info(result)

    def insert_mood_description(self, user, description, timestamp):
        mooddesc_col = self.database["mood_description"]
        new_mooddesc = {
            "userid": user,
            "description": description,
            "timestamp": timestamp,
        }
        result = mooddesc_col.insert(new_mooddesc)

        self.logger.info(result)

    def insert_mood_value(self, user, value, timestamp):
        moodvalue_col = self.database["mood_value"]
        new_moodvalue = {"userid": user, "value": value, "timestamp": timestamp}
        result = moodvalue_col.insert(new_moodvalue)
        self.logger.info(result)

    def get_mood_values(self, user):
        moodvalue_col = self.database["mood_value"]
        query = {"userid": user}
        result_docs = moodvalue_col.find(query)
        result = []
        for x in result_docs:
            result.append(x)
        self.logger.info(result)
        return result

    def insert_new_access_token(self, user):
        token_col = self.database["access_tokens"]
        existing_tokens_cursor = token_col.find()
        existing_tokens = []
        for token in existing_tokens_cursor:
            existing_tokens.append(token["token"])

        token = create_secret_token()
        while token in existing_tokens:
            token = create_secret_token()
        new_access_token_entry = {"userid": user, "token": token}
        result = token_col.insert(new_access_token_entry)
        self.logger.info(result)
        return token

    def diary_entry_exists_for_today(self, user, _timezone="Europe/Berlin"):
        # TODO do this check in users timezone

        diary_col = self.database["diary_entries"]
        current_time = datetime.now(pytz.utc)
        time_border = current_time.astimezone(timezone(_timezone))
        time_border = time_border.replace(minute=0, hour=0)
        time_border = time_border.astimezone(timezone("UTC"))

        query = {"userid": user, "timestamp": {"$gte": time_border}}
        result_docs = diary_col.find(query)
        result = []
        for x in result_docs:
            result.append(x)
        self.logger.info(
            "Diary entries already existing for today: " + str(len(result))
        )
        if len(result) > 0:
            return True
        else:
            return False
