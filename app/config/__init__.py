import os

__author__ = 'darryl'


class Config:
    DB_SERVER = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
    DB_PORT = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
    DB_NAME = os.environ.get("OPENSHIFT_APP_NAME")
    APP_STORAGE = os.environ.get("OPENSHIFT_DATA_DIR")

default = Config