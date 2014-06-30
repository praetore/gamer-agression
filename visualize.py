from nvd3 import multiBarChart, pieChart

from post_database import get_all_posts_by_topic
from user_database import get_all_users_by_topic


__author__ = 'Darryl'


def get_friendship_stats(population):
    pop_size = len(population)
    if pop_size == 0:
        return 0, 0, 0

    total_followers, total_friends, total_retweets = 0, 0, 0
    for i in population:
        total_followers += i['followers_count']
        total_friends += i['friends_count']
        total_retweets += i['retweet_on_post_count']

    average_followers_size = total_followers / pop_size
    average_friends_size = total_friends / pop_size
    average_retweets_size = float(total_retweets) / pop_size

    return average_followers_size, average_friends_size, average_retweets_size


def get_sentiment_stats(population):
    pop_size = len(population)
    if pop_size == 0:
        return 0, 0

    negative, positive = 0.0, 0.0
    for i in population:
        sentiment = i['post_sentiment']
        if sentiment == 'neg':
            negative += 1
        else:
            positive += 1

    percent_neg = negative / len(population) * 100
    percent_pos = positive / len(population) * 100

    return percent_pos, percent_neg


def generate_friends_chart(groups):
    chart = multiBarChart(width=500, height=400, x_axis_format=None)
    xdata = ["Followers per user", "Friends per user", "Retweets per post"]
    ydata = [[], []]

    for topics in groups:
        index = groups.index(topics)
        total_population = []
        for topic in topics:
            population = get_all_users_by_topic(topic)
            for p in population:
                total_population.append(p)

        y = ydata[index]
        follow, friend, retw = get_friendship_stats(total_population)
        y.append(follow)
        y.append(friend)
        y.append(retw)

    chart.add_serie(name="IMDB top games of 2014", y=ydata[0], x=xdata)
    chart.add_serie(name="Twitter trending topics", y=ydata[1], x=xdata)

    str(chart)
    return chart.content


def generate_sentiment_chart(topics, name):
    chart = pieChart(name=name, color_list=["green", "red"], height=400, width=400)
    xdata = ["Positive sentiment", "Negative sentiment"]
    ydata = []

    total_population = []
    for topic in topics:
        population = get_all_posts_by_topic(topic)
        for p in population:
            total_population.append(p)

    pos, neg = get_sentiment_stats(total_population)
    ydata.append(pos)
    ydata.append(neg)

    extra_serie = {"tooltip": {"y_start": "", "y_end": "%"}}
    chart.add_serie(name="IMDB top games of 2014", y=ydata, x=xdata, extra=extra_serie)

    str(chart)
    return chart.content