from urllib2 import urlopen

from bs4 import BeautifulSoup
from unidecode import unidecode
import unirest

from post_database import add_post
from user_database import add_user
from topic_database import add_topic, get_topic_by_name
from twitter_project import search_twitter, get_trending_twitter


__author__ = 'Darryl'


def get_trends_data():
    us_woe_id = 23424977
    trends_data = get_trending_twitter(us_woe_id)[0]['trends']
    trends = []
    for i in trends_data:
        trends.append(i['name'])
    return trends


def get_trending_games():
    url = "http://www.imdb.com/search/title?sort=moviemeter&title_type=game&year=2014,2014"
    html = urlopen(url).read()
    soup = BeautifulSoup(html)
    games_list = []
    exclude = ["X", "IMDb Pro", ""]
    for link in soup.find_all('a'):
        game_name = unidecode(link.get_text())
        if "/title/" in link.get('href') and game_name not in exclude and len(games_list) < 10:
            games_list.append(game_name)
    return games_list


def retrieve_data_from_twitter(subjects, game_related_data=False):
    store_topic_data(subjects, game_related_data)
    for subject in subjects:
        print "Retrieving data on", subject
        status_data = search_twitter(subject)
        store_user_data(status_data, subject, game_related_data)
        # store_post_data(status_data, subject, game_related_data)


def store_user_data(status_data, subject, game_related_data=False):
    user_list = []
    for i in status_data:
        if unidecode(i['lang']) == 'en' and i['retweeted']:
            user = i['user']
            user_name = unidecode(user['name'])

            user_item = {"_id": int(user['id']),
                         "user_name": user_name,
                         "gamer": game_related_data,
                         "subject": subject,
                         "followers_count": int(user['followers_count']),
                         "friends_count": int(user['friends_count']),
                         "retweet_on_post_count": int(i['retweet_count'])}

            if user_item not in user_list:
                add_user(user_item)
                user_list.append(user_item)


def store_post_data(status_data, subject, game_related_data=False):
    post_list = []
    for i in status_data:
        if unidecode(i['lang']):
            post_text = unidecode(i['text'])
            if post_text not in post_list:
                post_sentiment = get_sentiment_for_post(post_text)

                post_item = {"_id": int(i['id']),
                             "gamer": game_related_data,
                             "subject": subject,
                             "post_text": post_text,
                             "post_sentiment": post_sentiment}

                add_post(post_item)
                post_list.append(post_text)


def store_topic_data(subjects, game_related_data=False):
    for subject in subjects:
        if not get_topic_by_name(subject):
            add_topic({"subject": subject,
                       "game_data": game_related_data})


# Implement textblob since this is way too slow
def get_sentiment_for_post(status):
    response = unirest.post("https://japerk-text-processing.p.mashape.com/sentiment/",
                            headers={"X-Mashape-Key": "0w29CHi5IrmshzMhqjNZft1rByEXp1BBb69jsnfZ2qVKImPqV2"},
                            params={"language": "english", "text": status})

    return response.body['label']


def main():
    print "Retrieving list of topics"
    games_list = get_trending_games()
    trends = get_trends_data()

    print "Twitter trending topics"
    retrieve_data_from_twitter(trends)

    print "Popular videogames"
    retrieve_data_from_twitter(games_list, True)


if __name__ == '__main__':
    main()