from flask import Flask, render_template

from topic_database import get_latest_topics
from visualize import generate_friends_chart, generate_sentiment_chart


__author__ = 'Darryl'

app = Flask(__name__)


@app.route('/')
def index():
    games_list = get_latest_topics(True)
    trends = get_latest_topics()
    topics_list = [games_list, trends]
    friends_chart = generate_friends_chart(topics_list)
    sentiment_chart_games = generate_sentiment_chart(games_list, 'gamesChart')
    sentiment_chart_trends = generate_sentiment_chart(trends, 'trendsChart')
    return render_template('chart.html', friends_chart=friends_chart,
                           sentiment_chart_games=sentiment_chart_games,
                           sentiment_chart_trends=sentiment_chart_trends)

if __name__ == '__main__':
    app.run(debug=True)