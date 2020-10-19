import spacy

# if "Can't find model 'en_core_web_sm'" download it by using: python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

# Some names aren't recognized by spaCy. To ensure reliability of an experiment put the names of participants here
custom_names = {'PseudoName1', 'PseudoName2'}


# Named Entity Recognition using spaCy
def extract_person(text):
    global nlp
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    person = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            person = ent.text

    if person is None:
        for custom_name in custom_names:
            if custom_name.lower() in text.lower():
                person = custom_name
                break
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
