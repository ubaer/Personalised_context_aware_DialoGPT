import spacy

nlp = spacy.load("en_core_web_sm")


# Named Entity Recognition using spaCy
def extract_person(text):
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    person = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            person = ent.text
    return person


def extract_country(text):
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    country = None
    for ent in doc.ents:
        if ent.label_ == "GPE":
            # print(ent.text, ent.start_char, ent.end_char, ent.label_)
            country = ent.text
    return country
