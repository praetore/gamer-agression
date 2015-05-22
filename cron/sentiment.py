import os
import random
import pickle

import nltk.tokenize as tokenize
import nltk
from app import app


def bag_of_words(words):
    return dict((word, True) for word in words)


def document_features(document, word_features):
    features = {}
    for word in word_features:
        features[word] = (word in document)
    return features


def get_docs():
    movie_reviews = nltk.corpus.movie_reviews

    documents = [(set(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]

    random.seed(3)
    random.shuffle(documents)

    return documents


def get_word_features():
    movie_reviews = nltk.corpus.movie_reviews

    all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
    return all_words.keys()[:2000]


def get_classifier():
    binfile = os.path.join(app.config["APP_STORAGE"], 'classifier.pickle')
    try:
        with open(binfile, 'rb') as saved_cl:
            classifier = pickle.load(saved_cl)
    except (pickle.PickleError, IOError):
        word_features = get_word_features()
        train_set = [(document_features(d, word_features), c) for (d, c) in get_docs()]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        with open(binfile, 'wb') as saved_cl:
            pickle.dump(classifier, saved_cl)

    return classifier


def get_sentiment(classifier, text):
    words = tokenize.word_tokenize(text)
    feats = bag_of_words(words)
    return classifier.classify(feats)