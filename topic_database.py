from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from unidecode import unidecode

__author__ = 'Darryl'

server = 'localhost'
port = 27017


def connect():
    client = MongoClient('mongodb://' + server + ":" + str(port))
    db = client.project3
    collection = db.topics
    return collection


def add_topic(topic):
    collection = connect()
    try:
        collection.insert(topic)
    except DuplicateKeyError:
        pass


# TODO: Return ten latest stored topics
def get_latest_topics(game_related_data=False):
    collection = connect()
    topics = []
    for post in collection.find({"game_data": game_related_data}):
        topics.append(unidecode(post['subject']))
    return topics[:10]


def get_topic_by_id(topic_id):
    collection = connect()
    id_query = {"_id": topic_id}
    topic = collection.find_one(id_query)
    return topic


def get_topic_by_name(topic_name):
    collection = connect()
    name_query = {"_id": topic_name}
    topic = collection.find_one(name_query)
    return topic