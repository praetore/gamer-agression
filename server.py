import json
from flask import Flask, render_template
from member_database import find_all_by_subject
from test_data import get_stats, fetch_subject_data

__author__ = 'Darryl'

app = Flask(__name__)

@app.route('/')
def view_chart():
    return render_template('chart.html')

@app.route('/data')
def show_data():
    all_groups = [fetch_subject_data(True), fetch_subject_data()]
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
            population = find_all_by_subject(subject)
            avg_follow, avg_friends, avg_retw = get_stats(population)
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