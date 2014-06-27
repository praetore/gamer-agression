from bs4 import BeautifulSoup
from nvd3 import multiBarChart

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


def generate_friends_chart(groups):
    chart = multiBarChart(width=500, height=400, x_axis_format=None)
    xdata = ["Followers per user", "Friends per user", "Retweets per post"]
    ydata = [[], []]

    for subject in groups:
        index = groups.index(subject)
        total_population = []
        for i in subject:
            population = get_all_users_by_topic(i)
            for p in population:
                total_population.append(p)

        y = ydata[index]
        follow, friend, retw = get_friendship_stats(total_population)
        y.append(follow)
        y.append(friend)
        y.append(retw)

    chart.add_serie(name="IMDB top games of 2014", y=ydata[0], x=xdata)
    chart.add_serie(name="Twitter trending topics", y=ydata[1], x=xdata)

    chart_html = str(chart)
    chart_soup = BeautifulSoup(chart_html)
    html_data = chart_soup.body.find('div')
    html_chart = chart_soup.body.find('script')
    return html_data, html_chart