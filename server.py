import json

from flask import Flask, render_template

from topic_database import get_latest_topics
from user_database import get_all_users_by_topic
from visualize import generate_friends_chart, get_friendship_stats, generate_sentiment_chart


__author__ = 'Darryl'

app = Flask(__name__)


@app.route('/')
def view_chart():
    games_list = get_latest_topics(True)
    trends = get_latest_topics()
    topics_list = [games_list, trends]
    friends_chart = generate_friends_chart(topics_list)
    sentiment_chart = generate_sentiment_chart(topics_list)
    return render_template('chart.html', friends_chart=friends_chart, sentiment_chart=sentiment_chart)


@app.route('/data')
def show_data():
    all_groups = [get_latest_topics(True), get_latest_topics()]
    data = [{"key": "IMDB top games of 2014", "values": []},
            {"key": "Twitter trending topics", "values": []}]
    for subjects in all_groups:
        index = all_groups.index(subjects)
        current_list = data[index]['values']
        key_follow = "Followers per user"
        key_friends = "Friends per user"
        key_retweets = "Retweets per post"
        current_list.append({"key": key_follow, "values": []})
        current_list.append({"key": key_friends, "values": []})
        current_list.append({"key": key_retweets, "values": []})
        for subject in subjects:
            population = get_all_users_by_topic(subject)
            avg_follow, avg_friends, avg_retw = get_friendship_stats(population)
            for list_item in current_list:
                value_to_add = {'label': subject, 'value': 0}
                if list_item['key'] == key_follow:
                    value_to_add['value'] = avg_follow
                elif list_item['key'] == key_friends:
                    value_to_add['value'] = avg_friends
                elif list_item['key'] == key_retweets:
                    value_to_add['value'] = avg_retw
                list_item['values'].append(value_to_add)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)