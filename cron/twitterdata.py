import os

# Python Twitter Tools, functies voor Twitter, download op
# http://mike.verdone.ca/twitter/

# Importeer libraries van Twitter-module
import twitter
from twitter.oauth import write_token_file, read_token_file
from twitter.oauth_dance import oauth_dance

# Maak OAuth-gegevens aan
# Check https://dev.twitter.com/apps, and in an application,
# go to OAuth tool

app_name = os.environ.get("TWITTER_APPNAME")
cons_key = os.environ.get("TWITTER_KEY")
cons_secret = os.environ.get("TWITTER_SECRET")

TOKEN_FILE = os.path.join(os.environ.get("OPENSHIFT_DATA_DIR"), "out", "twitter.oauth")  # Don't change this!


def auth_twitter():
    # Verifieer OAuth-gegevens
    try:
        # Lees OAuth gegevens in van bestand op harde-schijf
        (token, token_secret) = read_token_file(TOKEN_FILE)
    except IOError:
        # Als het bestand niet aanwezig is, maak nieuwe gegevens aan
        (token, token_secret) = oauth_dance(app_name, cons_key,
                                            cons_secret)

        token_folder = os.path.join(os.environ.get("OPENSHIFT_DATA_DIR"), "out")
        # Maak een map aan genaamd 'out'
        if not os.path.isdir(token_folder):
            os.mkdir(token_folder)

        # Schrijf OAuth-gegevens weg naar bestand op harde-schijf in map 'out'
        write_token_file(TOKEN_FILE, token, token_secret)

    # Maak variabelen aan voor OAuth-verificatie op Twitter
    verification = twitter.oauth.OAuth(token, token_secret, cons_key, cons_secret)
    t = twitter.Twitter(auth=verification)

    return t


def search_twitter(q, max_results=200, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and
    # https://dev.twitter.com/docs/using-search for details on advanced
    # search criteria that may be useful for keyword arguments

    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    t = auth_twitter()
    search_results = t.search.tweets(q=q, count=100, **kw)

    statuses = search_results['statuses']

    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.

    # Enforce a reasonable limit
    max_results = min(1000, max_results)

    for _ in range(10):  # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError:  # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([kv.split('=')
                       for kv in next_results[1:].split("&")])

        search_results = t.search.tweets(**kwargs)
        statuses += search_results['statuses']

        if len(statuses) > max_results:
            break

    return statuses


def get_trending_twitter(woe_id=1):
    return auth_twitter().trends.place(_id=woe_id)