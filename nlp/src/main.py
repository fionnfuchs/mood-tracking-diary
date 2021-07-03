import spacy
from nltk.stem.snowball import SnowballStemmer
from mock_data import mock_diary_entries, mock_mood_values

en_nlp = spacy.load("en_core_web_sm")
de_nlp = spacy.load("de_core_news_sm")


def analyze_entries(entries, language):  # Analyze all entries of one day
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
                if token.dep_ == "ROOT" or token.dep_ == "conj":
                    relevant_verbs.append(token.lemma_)

            if token.pos_ == "NOUN":
                if token.dep_ == "pobj":
                    relevant_nouns.append(token.lemma_)

    return {"relevant_verbs": relevant_verbs, "relevant_nouns": relevant_nouns}


def main():
    entries = filter(lambda x: x["timestamp"] == 0, mock_diary_entries)
    print(analyze_entries(entries, "en"))


if __name__ == "__main__":
    main()
