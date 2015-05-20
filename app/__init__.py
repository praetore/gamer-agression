from flask import Flask

from app.charts import generate_friends_chart, generate_sentiment_chart, generate_distribution_chart


__author__ = 'Darryl'

app = Flask(__name__)
