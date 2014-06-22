from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from unidecode import unidecode

__author__ = 'Darryl'

server = 'localhost'
port = 27017


def connect():
    client = MongoClient('mongodb://' + server + ":" + str(port))
    db = client.project3
    collection = db.subject_data
    return collection


def add_subject(subject):
    collection = connect()
    try:
        collection.insert(subject)
    except DuplicateKeyError:
        pass


def find_ten(game_related_data=False):
    collection = connect()
    members = []
    for post in collection.find({"game_data": game_related_data}):
        members.append(unidecode(post['subject']))
    return members[:10]


def find_all():
    collection = connect()
    members = []
    for post in collection.find():
        members.append(post)
    return members


def find_by_id(subject_id):
    collection = connect()
    id_query = {"_id": subject_id}
    member = collection.find_one(id_query)
    return member