from bson import ObjectId
from pymongo import MongoClient

__author__ = 'Darryl'

server = 'localhost'
port = 27017


def connect():
    client = MongoClient('mongodb://' + server + ":" + str(port))
    db = client.project3
    collection = db.tweets
    return collection


def add_tweet(post):
    collection = connect()
    post_id = collection.insert(post)
    return post_id


def find_all():
    collection = connect()
    posts = []
    for post in collection.find():
        posts.append(post)
    return posts


def find_by_id(post_id):
    collection = connect()
    id_query = {"_id": ObjectId(post_id)}
    post = collection.find_one(id_query)
    return post