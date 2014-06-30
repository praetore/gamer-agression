from sentiment import get_classifier, get_sentiment

__author__ = 'Darryl'


with open("pos1.txt") as f:
    text = f.read()

cl = get_classifier()
print get_sentiment(cl, text)