from flask import render_template
from app import app
from app.charts import generate_friends_chart, generate_sentiment_chart, generate_distribution_chart
from app.database import get_latest_topics


@app.route('/')
def index():
    games_list = get_latest_topics(True)
    trends = get_latest_topics()
    topics_list = [games_list, trends]
    social_interaction = generate_friends_chart(topics_list)

    sentiment = [generate_sentiment_chart(games_list, 'gamesChart'),
                 generate_sentiment_chart(trends, 'trendsChart')]

    distribution_followers = [generate_distribution_chart(games_list,
                                                          "gamerFollowersDist",
                                                          "followers_count", 10, 10),
                              generate_distribution_chart(trends,
                                                          "nGamerFollowersDist",
                                                          "followers_count", 10, 10)]

    distribution_friends = [generate_distribution_chart(games_list,
                                                        "gamerFriendsDist",
                                                        "friends_count", 10, 10),
                            generate_distribution_chart(trends,
                                                        "nGamerFriendsDist",
                                                        "friends_count", 10, 10)]

    distribution_retweets = [generate_distribution_chart(games_list,
                                                         "gamerRetweetDist",
                                                         "retweet_on_post_count", 0.01, 10, True),
                             generate_distribution_chart(trends,
                                                         "nGamerRetweetDist",
                                                         "retweet_on_post_count", 0.01, 10, True)]

    return render_template('chart.html', social_interaction=social_interaction,
                           sentiment=sentiment,
                           distribution_followers=distribution_followers,
                           distribution_friends=distribution_friends,
                           distribution_retweets=distribution_retweets)