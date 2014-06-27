from prettytable import PrettyTable

from post_database import get_all_posts_by_topic
from topic_database import get_latest_topics
from user_database import get_all_users_by_topic
from visualize import get_friendship_stats, get_sentiment_stats


__author__ = 'Darryl'


def present_friendship_data(terms, game_related_data=False):
    column_names = ["", "Followers per user",
                    "Friends per user",
                    "Retweets per user"]
    if game_related_data:
        subject = "IMDB top games of 2014"
    else:
        subject = "Twitter trending topics"
    column_names[0] = subject

    table = PrettyTable(column_names)
    table.align[subject] = "l"

    total_population = []
    for i in terms:
        population = get_all_users_by_topic(i)
        for p in population:
            total_population.append(p)
        avg_follow, avg_friends, avg_retw = get_friendship_stats(population)
        if avg_follow != 0 and avg_friends != 0:
            table.add_row([i, avg_follow, avg_friends, avg_retw])

    total_followers, total_friends, total_retweets = get_friendship_stats(total_population)
    table.add_row(["Average of group", total_followers, total_friends, total_retweets])
    print table


def present_sentiment_data(terms, game_related_data=False):
    column_names = ["", "Positive sentiment",
                    "Negative sentiment"]
    if game_related_data:
        subject = "IMDB top games of 2014"
    else:
        subject = "Twitter trending topics"
    column_names[0] = subject

    table = PrettyTable(column_names)
    table.align[subject] = "l"

    total_population = []
    for i in terms:
        population = get_all_posts_by_topic(i)
        for p in population:
            total_population.append(p)
        pos, neg = get_sentiment_stats(population)
        table.add_row([i, pos, neg])

    print table


def main():
    trends = get_latest_topics()
    games_list = get_latest_topics(True)

    present_friendship_data(trends)
    present_friendship_data(games_list, True)

    # present_sentiment_data(trends)
    # present_sentiment_data(games_list, True)


if __name__ == '__main__':
    main()