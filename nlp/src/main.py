import spacy
from nltk.stem.snowball import SnowballStemmer
from mock_data import mock_diary_entries, mock_mood_values
import sched, time
from data_service import DataService
import logging

en_nlp = spacy.load("en_core_web_sm")
de_nlp = spacy.load("de_core_news_sm")

mongodb_data_service = DataService()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

nlp_schedule_init_time = 10
nlp_schedule_loop_time = 60


def analyze_entries(entries, language):  # Analyze all entries of one day
    logger.info(" ---- " + language)

    if language == "de":
        nlp = de_nlp
    else:
        nlp = en_nlp

    relevant_verbs = []
    relevant_nouns = []

    for entry in entries:
        doc = nlp(entry["entry"])

        for token in doc:
            if token.pos_ == "VERB":
                if language == "en":
                    if token.dep_ == "ROOT" or token.dep_ == "conj":
                        relevant_verbs.append(token.lemma_)
                if language == "de":
                    if token.dep_ == "ROOT" or token.dep_ == "oc":
                        relevant_verbs.append(token.lemma_)

            if token.pos_ == "NOUN":
                if language == "en":
                    if token.dep_ == "pobj":
                        relevant_nouns.append(token.lemma_)
                if language == "de":
                    if token.dep_ == "nk":
                        relevant_nouns.append(token.lemma_)

    return {"relevant_verbs": relevant_verbs, "relevant_nouns": relevant_nouns}


def run_schedule(sc):
    logger.info("Running NLP schedule...")
    users = mongodb_data_service.get_active_users()
    for user in users:
        logger.info(" -- Analyzing entries of user " + str(user["userid"]))
        diary_entries = mongodb_data_service.get_diary_entries(user["userid"])
        # TODO: Group diary entries and mood values by date
        # TODO: Analyze grouped diary entries and assign mood values of same date
        analysis = analyze_entries(diary_entries, user["language"])
        logger.info(" ---- Analysis" + str(analysis))
    s.enter(nlp_schedule_loop_time, 1, run_schedule, (sc,))


def run_mock():
    entries = filter(lambda x: x["timestamp"] == 0, mock_diary_entries)
    print(analyze_entries(entries, "en"))


if __name__ == "__main__":
    mongodb_data_service.connect()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(nlp_schedule_init_time, 1, run_schedule, (s,))
    s.run()
