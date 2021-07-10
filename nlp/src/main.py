import spacy
from nltk.stem.snowball import SnowballStemmer
from mock_data import mock_diary_entries, mock_mood_values
import sched, time
from data_service import DataService
import logging
import datetime

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
        mood_values = mongodb_data_service.get_mood_values(user["userid"])

        data_by_date = {}
        data_by_date = group_diary_entries_by_date(diary_entries, data_by_date)
        data_by_date = group_mood_values_by_date(mood_values, data_by_date)

        analysis = analyze_data_by_date(data_by_date, user["language"])

        mongodb_data_service.update_nlp_analysis(analysis, user["userid"])

        logger.info(" ---- Analysis written to MongoDB: " + str(analysis))
    sc.enter(nlp_schedule_loop_time, 1, run_schedule, (sc,))


def analyze_data_by_date(data_by_date, language):
    analysis = {"verbs": {}, "nouns": {}}
    for date in data_by_date.keys():
        nlp_dict = analyze_entries(data_by_date[date]["entries"], language)
        for verb in nlp_dict["relevant_verbs"]:
            for value in data_by_date[date]["values"]:
                if verb not in analysis["verbs"].keys():
                    analysis["verbs"][verb] = [value]
                else:
                    analysis["verbs"][verb].append(value)
        for noun in nlp_dict["relevant_nouns"]:
            for value in data_by_date[date]["values"]:
                if noun not in analysis["nouns"].keys():
                    analysis["nouns"][noun] = [value]
                else:
                    analysis["nouns"][noun].append(value)

    return analysis


def date_of_timestamp(timestamp):
    return timestamp.strftime("%d-%m-%Y")


def group_diary_entries_by_date(diary_entries, target_dict):
    for entry in diary_entries:
        key = date_of_timestamp(entry["timestamp"])
        if key not in target_dict.keys():
            target_dict[key] = {"entries": [entry], "values": []}
        else:
            target_dict[key]["entries"].append(entry)

    return target_dict


def group_mood_values_by_date(mood_values, target_dict):
    for value in mood_values:
        key = date_of_timestamp(value["timestamp"])
        if key not in target_dict.keys():
            target_dict[key] = {"entries": [], "values": [value["value"]]}
        else:
            target_dict[key]["values"].append(value["value"])

    return target_dict


def run_mock():
    entries = filter(lambda x: x["timestamp"] == 0, mock_diary_entries)
    print(analyze_entries(entries, "en"))


if __name__ == "__main__":
    mongodb_data_service.connect()
    s = sched.scheduler(time.time, time.sleep)
    s.enter(nlp_schedule_init_time, 1, run_schedule, (s,))
    s.run()
