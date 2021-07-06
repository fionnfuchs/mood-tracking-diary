import pymongo
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


class DataService:
    def __init__(self):
        self.client = None
        self.database = None

    def connect(self):
        self.client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.database = self.client["userdata"]
        logger.info("Database successfully connected!")

    def get_mood_values(self, userid):
        moodvalue_col = self.database["mood_value"]
        query = {"userid": userid}
        result_docs = moodvalue_col.find(query)
        result = []
        for x in result_docs:
            result.append(x)
        return result

    def get_diary_entries(self, userid):
        moodvalue_col = self.database["diary_entries"]
        query = {"userid": userid}
        result_docs = moodvalue_col.find(query)
        result = []
        for x in result_docs:
            result.append(x)
        return result

    def get_active_users(self):
        user_col = self.database["users"]
        result_docs = user_col.find()
        result = []
        for user in result_docs:
            result.append(user)
        return result

    def update_nlp_analysis(self, analysis, userid):
        nlp_analysis_col = self.database["nlp_analysis"]
        result = nlp_analysis_col.update(
            {"userid": userid}, {"$set": analysis}, upsert=True
        )
        logger.info(result)