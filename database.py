from bson import ObjectId
from pymongo import MongoClient
from bson.json_util import dumps

__author__ = 'Darryl'

server = 'localhost'
port = 27017


def connect():
    client = MongoClient('mongodb://' + server + ":" + str(port))
    db = client.project3
    collection = db.members_data
    return collection


def add_subject_members(members):
    collection = connect()
    current = find_all()

    #avoiding duplication
    for i in current:
        del i['_id']
    for i in members:
        if i in current:
            members.remove(i)
            current.remove(i)

    collection.insert(members)


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
    id_query = {"_id": ObjectId(member_id)}
    member = collection.find_one(id_query)
    return member