from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

import config


__author__ = 'Darryl'

server = config.server
port = config.port
database = config.database


def connect():
    uri = 'mongodb://' + server + ":" + str(port)
    client = MongoClient(uri)
    db = client[database]
    collection = db.users
    return collection


def add_user(user):
    collection = connect()
    try:
        collection.insert(user)
    except DuplicateKeyError:
        pass


def get_all_users_by_topic(subject):
    collection = connect()
    users = []
    for post in collection.find({"subject": subject}):
        users.append(post)
    return users


def get_all_users():
    collection = connect()
    users = []
    for post in collection.find():
        users.append(post)
    return users


def get_user_by_id(member_id):
    collection = connect()
    id_query = {"_id": member_id}
    user = collection.find_one(id_query)
    return user