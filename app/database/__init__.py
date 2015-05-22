from pymongo import MongoClient
from unidecode import unidecode
from app import app

__author__ = 'darryl'


def connect():
    db_name = app.config.get("DB_NAME")
    db_url = app.config.get("DB_URL")
    client = MongoClient(db_url)
    db = client[db_name]
    return db


def retrieve_by_id(req_id, collname=None):
    db = connect()
    collection = db[collname]
    id_query = {"_id": req_id}
    res = collection.find_one(id_query)
    return res


def retrieve_by_topic(topic, collname=None):
    db = connect()
    collection = db[collname]
    res = []
    for i in collection.find({"topic": topic}):
        res.append(i)
    return res


def retrieve_all(collname=None):
    db = connect()
    collection = db[collname]
    res = [i for i in collection.find()]
    return res


def get_latest_topics(game_related_data=False):
    db = connect()
    collection = db.topics
    topics = []
    for post in collection.find({"game_data": game_related_data, }).sort("date_added", 1):
        topics.append(unidecode(post['topic']))
    return topics[:10]