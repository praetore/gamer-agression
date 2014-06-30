import pprint
from twitter_project import search_twitter

__author__ = 'Darryl'

tweets = search_twitter('gta5')
print pprint.pprint(tweets[0])