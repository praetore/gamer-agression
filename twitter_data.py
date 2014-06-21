from urllib2 import urlopen
from bs4 import BeautifulSoup
from database import add_subject_members, find_all_by_subject
from twitter_project import search_twitter, get_trending_twitter
from unidecode import unidecode
from prettytable import PrettyTable

__author__ = 'Darryl'


def store_subject_data(subjects, game_related_data=False):
    for i in subjects:
        store_status_data(i, game_related_data)


def store_status_data(query, game_related_data=False):
    status_data = search_twitter(query)
    user_list = []
    for i in status_data:
        user = i['user']
        user_list.append({"user": unidecode(user['name']),
                            "gamer": game_related_data,
                            "subject": query,
                            "followers_count": int(user['followers_count']),
                            "friends_count": int(user['friends_count']),
                            "retweet_count": int(i['retweet_count'])})
    add_subject_members(user_list)


def get_stats(population, summary=False):
    pop_size = len(population)
    if pop_size == 0:
        return 0, 0, 0

    total_followers, total_friends, total_retweets = 0, 0, 0
    if not summary:
        for i in population:
            total_followers += i['followers_count']
            total_friends += i['friends_count']
            total_retweets += i['retweet_count']
    #TODO: Add statistics for whole group

    average_followers_size = total_followers / pop_size
    average_friends_size = total_friends / pop_size
    average_retweets_size = total_retweets / pop_size

    return average_followers_size, average_friends_size, average_retweets_size


def present_data_for_group(terms, game_related_data=False):
    column_names = ["", "Followers per user",
                    "Friends per user",
                    "Retweets per user"]
    if game_related_data:
        subject = "IMDB top games of 2014"
    else:
        subject = "Current Twitter trending topics"
    column_names[0] = subject

    table = PrettyTable(column_names)
    table.align[subject] = "l"

    for i in terms:
        population = find_all_by_subject(i)
        avg_follow, avg_friends, avg_retw = get_stats(population)
        if avg_follow != 0 and avg_friends != 0:
            table.add_row([i, avg_follow, avg_friends, avg_retw])

    print table


def get_trends_data():
    trends_data = get_trending_twitter()[0]['trends']
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


def main():
    trends = get_trends_data()
    games_list = get_trending_games()

    #store_subject_data(games_list, True)
    #store_subject_data(trends)

    present_data_for_group(trends)
    present_data_for_group(games_list)


if __name__ == '__main__':
    main()