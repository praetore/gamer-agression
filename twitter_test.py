import pprint
from twitter_project import search_twitter

__author__ = 'Darryl'


def main():
    pprint.pprint(search_twitter('gta5')[0]['user'])


if __name__ == '__main__':
    main()