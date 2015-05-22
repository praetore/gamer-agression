#!/usr/bin/env python
import hashlib
import os
import arrow
from bs4 import BeautifulSoup
from datetime import date
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import requests
from unidecode import unidecode

from sentiment import get_sentiment, get_classifier
from twitterdata import get_trending_twitter, search_twitter


__author__ = 'Darryl'

DB_SERVER = os.environ.get("OPENSHIFT_MONGODB_DB_HOST")
DB_PORT = os.environ.get("OPENSHIFT_MONGODB_DB_PORT")
DB_NAME = os.environ.get("OPENSHIFT_APP_NAME")


def connect():
    uri = 'mongodb://' + DB_SERVER + ":" + str(DB_PORT)
    client = MongoClient(uri)
    db = client[DB_NAME]
    return db


def add_to_db(obj, dbname):
    db = connect()
    collection = db[dbname]
    try:
        collection.insert(obj)
    except DuplicateKeyError:
        pass


def get_trends_data():
    us_woe_id = 23424977
    trends_data = get_trending_twitter(us_woe_id)[0]['trends']
    trends = []
    for i in trends_data:
        trends.append(i['name'])
    return trends


def get_trending_games():
    url = "http://www.imdb.com/search/title?sort=moviemeter&title_type=game&year={0},{0}".format(date.today().year)
    html = requests.get(url).text
    soup = BeautifulSoup(html)
    games_list = []
    exclude = ["X", "IMDb Pro", ""]
    for link in soup.find_all('a'):
        game_name = unidecode(link.get_text())
        if "/title/" in link.get('href') and game_name not in exclude and len(games_list) < 10:
            games_list.append(game_name)
    return games_list


def retrieve_data_from_twitter(classifier, topics, game_related_data=False):
    store_topic_data(topics, game_related_data)
    for topic in topics:
        print("Retrieving data on {}".format(topic))
        status_data = search_twitter(topic)
        store_user_data(status_data, topic, game_related_data)
        store_post_data(classifier, status_data, topic, game_related_data)


def store_user_data(status_data, topic, game_related_data=False):
    user_list = []
    for i in status_data:
        if unidecode(i['lang']) == 'en':
            user = i['user']
            user_name = unidecode(user['name'])

            user_item = {"_id": int(user['id']),
                         "user_name": user_name,
                         "gamer": game_related_data,
                         "topic": topic,
                         "followers_count": int(user['followers_count']),
                         "friends_count": int(user['friends_count']),
                         "retweet_on_post_count": int(i['retweet_count'])}
            if user_item not in user_list:
                add_to_db(user_item, "users")
                user_list.append(user_item)


def store_post_data(classifier, status_data, topic, game_related_data=False):
    post_list = []
    for i in status_data:
        if unidecode(i['lang']):
            post_text = unidecode(i['text'])
            if post_text not in post_list:
                post_sentiment = get_sentiment(classifier, post_text)

                post_item = {"_id": int(i['id']),
                             "gamer": game_related_data,
                             "topic": topic,
                             "post_text": post_text,
                             "post_sentiment": post_sentiment}

                add_to_db(post_item, "posts")
                post_list.append(post_text)


def store_topic_data(topics, game_related_data=False):
    h = hashlib.sha1()
    for topic in topics:
        utc = arrow.utcnow()
        add_to_db({
            "_id": h.update(topic).hexdigest(),
            "topic": topic,
            "date_added": utc.to('Europe/Amsterdam').timestamp,
            "game_data": game_related_data}, "topics")


def main():
    print("Retrieving list of popular games")
    games_list = get_trending_games()
    print(games_list)

    print("Retrieving list of trending topics")
    trends = get_trends_data()
    print(trends)

    print("Training classifier")
    classifier = get_classifier()

    print("Twitter trending topics")
    retrieve_data_from_twitter(classifier, trends)

    print("Popular videogames")
    retrieve_data_from_twitter(classifier, games_list, True)


if __name__ == '__main__':
    main()