from pymongo import MongoClient, Connection
import config

__author__ = 'Darryl'

server = config.server
port = config.port

uri = 'mongodb://' + server + ":" + str(port)
conn = MongoClient(uri)
print conn.gameragression
print conn.server_info()