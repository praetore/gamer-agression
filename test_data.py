from prettytable import PrettyTable

from topic_database import get_latest_topics
from user_database import get_all_users_by_topic
from visualize import get_friendship_stats


__author__ = 'Darryl'


def present_data_for_group(terms, game_related_data=False):
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


def main():
    trends = get_latest_topics()
    games_list = get_latest_topics(True)

    present_data_for_group(games_list, True)
    present_data_for_group(trends)


if __name__ == '__main__':
    main()