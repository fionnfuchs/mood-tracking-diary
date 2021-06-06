import pymongo
from tokens import create_secret_token


class DataService:
    def __init__(self, logger):
        self.client = None
        self.database = None
        self.logger = logger

    def connect(self):
        self.client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.database = self.client["userdata"]

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
