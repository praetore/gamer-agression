from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from unidecode import unidecode
from app import app

__author__ = 'darryl'


server = app.config["DB_SERVER"]
port = app.config["DB_PORT"]
database = app.config["DB_NAME"]


def connect():
    uri = 'mongodb://' + server + ":" + str(port)
    client = MongoClient(uri)
    db = client[database]
    return db


def add_to_db(obj, dbname=None):
    db = connect()
    collection = db[dbname]
    try:
        collection.insert(obj)
    except DuplicateKeyError:
        pass


def retrieve_by_id(req_id, dbname=None):
    db = connect()
    collection = db[dbname]
    id_query = {"_id": req_id}
    res = collection.find_one(id_query)
    return res


def retrieve_by_topic(topic, dbname=None):
    db = connect()
    collection = db[dbname]
    res = []
    for i in collection.find({"topic": topic}):
        res.append(i)
    return res


def retrieve_all(dbname=None):
    db = connect()
    collection = db[dbname]
    res = [i for i in collection.find()]
    return res


def get_latest_topics(game_related_data=False):
    db = connect()
    collection = db.topics
    topics = []
    for post in collection.find({"game_data": game_related_data, }).sort("date_added", 1):
        topics.append(unidecode(post['topic']))
    return topics[:10]