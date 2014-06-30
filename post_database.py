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
    collection = db.posts
    return collection


def add_post(post):
    collection = connect()
    try:
        collection.insert(post)
    except DuplicateKeyError:
        pass


def get_all_posts(game_related_data=False):
    collection = connect()
    posts = []
    for post in collection.find():
        posts.append(post)
    return posts


def get_all_posts_by_topic(subject):
    collection = connect()
    posts = []
    for post in collection.find({"subject": subject}):
        posts.append(post)
    return posts


def get_post_by_id(subject_id):
    collection = connect()
    id_query = {"_id": subject_id}
    post = collection.find_one(id_query)
    return post