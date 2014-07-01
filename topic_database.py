from pymongo import MongoClient
from unidecode import unidecode

import config


__author__ = 'Darryl'

server = config.server
port = config.port
database = config.database


def connect():
    uri = 'mongodb://' + server + ":" + str(port)
    client = MongoClient(uri)
    db = client[database]
    collection = db.topics
    return collection


def add_topic(topic):
    collection = connect()
    if not get_topic_by_name(topic['subject']):
        collection.insert(topic)
    else:
        pass


def get_latest_topics(game_related_data=False):
    collection = connect()
    topics = []
    for post in collection.find({"game_data": game_related_data}).sort("date_added", 1):
        if len(topics) != 10:
            topics.append(unidecode(post['subject']))
    return topics


def get_topic_by_id(topic_id):
    collection = connect()
    id_query = {"_id": topic_id}
    topic = collection.find_one(id_query)
    return topic


def get_topic_by_name(topic_name):
    collection = connect()
    name_query = {"subject": topic_name}
    topic = collection.find_one(name_query)
    return topic