import fasttext
import numpy as np
import scipy.spatial.distance


def load_fasttext_model():
    global fasttext_model
    fasttext_model = fasttext.load_model("models/FastText/yahoo_answers.bin")
    # This is for when you want to run this file stand alone
    # fasttext_model = fasttext.load_model("../models/FastText/yahoo_answers.bin")


def calculate_sentence_mean(sentence):
    if fasttext_model is not None:
        sentence_mean = np.mean([fasttext_model[x] for word in sentence for x in word.split()], axis=0)
        return sentence_mean
    else:
        print("load_model() not called yet")
        raise Exception


def cos_similarity(data_1, data_2):
    if fasttext_model is not None:
        return 1 - scipy.spatial.distance.cosine(data_1, data_2)
    else:
        print("load_model() not called yet")
        raise Exception


def get_most_similar_sentence_fasttext(baseline_sentence, other_sentences):
    baseline_sentence_mean = calculate_sentence_mean(baseline_sentence)
    print("Baseline sentence: " + baseline_sentence)
    best_similarity = 0
    best_sentence = ""

    for sentence in other_sentences:
        sentence_mean = calculate_sentence_mean(sentence)
        similarity = cos_similarity(baseline_sentence_mean, sentence_mean)
        print("Similarity: '" + sentence + "' = " + str(similarity))
        if (similarity != 1):
            if (best_similarity < similarity):
                best_similarity = similarity
                best_sentence = sentence
    return best_sentence

# a = "How are you doing?"
# b = "I'm doing great"
# c = "I like to drive cars"
#
# load_fasttext_model()
# get_most_similar_sentence(a, {b, c})
