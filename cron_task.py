from urllib2 import urlopen
from bs4 import BeautifulSoup
from nvd3 import multiBarChart
from unidecode import unidecode
from member_database import add_user, find_all_by_subject
from subject_database import add_subject, find_ten
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


def store_subjects(subject_list, game_related_data=False):
    for i in subject_list:
        add_subject({"subject": i, "game_data": game_related_data})


def store_subject_data(subjects, game_related_data=False):
    for i in subjects:
        store_status_data(i, game_related_data)


def store_status_data(query, game_related_data=False):
    status_data = search_twitter(query)
    user_list = []

    for i in status_data:
        user = i['user']
        user_item = {"_id": int(user['id']),
                     "user_name": unidecode(user['name']),
                     "gamer": game_related_data,
                     "subject": query,
                     "followers_count": int(user['followers_count']),
                     "friends_count": int(user['friends_count']),
                     "retweet_on_post_count": int(i['retweet_count'])}

        if user_item not in user_list:
            add_user(user_item)
            user_list.append(user_item)


def get_stats(population):
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
    average_retweets_size = total_retweets / pop_size

    return average_followers_size, average_friends_size, average_retweets_size


def generate_chart(groups):
    chart = multiBarChart(width=500, height=400, x_axis_format=None)
    xdata = ["Followers per user", "Friends per user", "Retweets per post"]
    ydata = [[], []]

    for subject in groups:
        index = groups.index(subject)
        total_population = []
        for i in subject:
            population = find_all_by_subject(i)
            for p in population:
                total_population.append(p)

        y = ydata[index]
        follow, friend, retw = get_stats(total_population)
        y.append(follow)
        y.append(friend)
        y.append(retw)

    chart.add_serie(name="IMDB top games of 2014", y=ydata[0], x=xdata)
    chart.add_serie(name="Twitter trending topics", y=ydata[1], x=xdata)

    with open('templates/chart.html', 'r') as f:
        output_html = str(f.read())

    with open('templates/chart.html', 'w') as f:
        output_soup = BeautifulSoup(output_html)
        chart_html = str(chart)
        chart_soup = BeautifulSoup(chart_html)
        output_soup.body = []
        output_soup.body.append(chart_soup.body.find('div'))
        output_soup.body.append(chart_soup.body.find('script'))
        f.write(str(output_soup))


def fetch_subject_data(game_related_data=False):
    return find_ten(game_related_data)


def main():
    # trends = get_trends_data()
    # games_list = get_trending_games()
    #
    # store_subjects(trends)
    # store_subjects(games_list, True)
    #
    # store_subject_data(games_list, True)
    # store_subject_data(trends)

    games_list = fetch_subject_data(True)
    trends = fetch_subject_data()

    generate_chart([games_list, trends])

if __name__ == '__main__':
    main()