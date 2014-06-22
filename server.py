import json
from flask import Flask
from twitter_data import fetch_status_data, get_stats, fetch_subjects

__author__ = 'Darryl'

app = Flask(__name__)


@app.route('/data')
def show_data():
    subject_list = [fetch_subjects(True), fetch_subjects()]
    data = [{"Popular games": []}, {"Popular trending topics": []}]
    for subject in subject_list:
        index = subject_list.index(subject)
        for i in subject:
            population = fetch_status_data(i)
            avg_follow, avg_friends, avg_retw = get_stats(population)
            game = {"Game": i,
                    "Followers": avg_follow,
                    "Friends": avg_friends,
                    "Retweets on post": avg_retw}
            data[index].values()[0].append(game)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(debug=True)