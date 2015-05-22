import os

__author__ = 'darryl'


class Config:
    DB_SERVER = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
    DB_PORT = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
    DB_NAME = os.environ.get("OPENSHIFT_APP_NAME")
    DB_URL = os.environ.get("OPENSHIFT_MONGODB_DB_URL")

default = Config