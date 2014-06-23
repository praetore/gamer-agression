from cron_task import fetch_subject_data, get_stats
from member_database import find_all_by_subject
from prettytable import PrettyTable

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
        population = find_all_by_subject(i)
        for p in population:
            total_population.append(p)
        avg_follow, avg_friends, avg_retw = get_stats(population)
        if avg_follow != 0 and avg_friends != 0:
            table.add_row([i, avg_follow, avg_friends, avg_retw])

    total_followers, total_friends, total_retweets = get_stats(total_population)
    table.add_row(["Average of group", total_followers, total_friends, total_retweets])
    print table


def main():
    trends = fetch_subject_data()
    games_list = fetch_subject_data(True)

    present_data_for_group(games_list, True)
    present_data_for_group(trends)


if __name__ == '__main__':
    main()