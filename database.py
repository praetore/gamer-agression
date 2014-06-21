from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

__author__ = 'Darryl'

server = 'localhost'
port = 27017


def connect():
    client = MongoClient('mongodb://' + server + ":" + str(port))
    db = client.project3
    collection = db.members_data
    return collection


def add_user(member):
    collection = connect()
    try:
        collection.insert(member)
    except DuplicateKeyError:
        pass


def find_all_by_subject(subject):
    collection = connect()
    members = []
    for post in collection.find({"subject": subject}):
        members.append(post)
    return members


def find_all():
    collection = connect()
    members = []
    for post in collection.find():
        members.append(post)
    return members


def find_by_id(member_id):
    collection = connect()
    id_query = {"_id": member_id}
    member = collection.find_one(id_query)
    return member