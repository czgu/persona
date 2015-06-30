import requests
import re
import sys
from collections import Counter
from settings import access_token

# Default paging is 25 so put limit to something high (100 just for test)
# Returns array of status info (has eg. id, message, updated_time, tags, comments)
def get_status_list(userid):
    endpoint = "https://graph.facebook.com/v2.3/{0}/statuses".format(userid)
    url = "{0}?access_token={1}&limit=100".format(endpoint, access_token)
    r = requests.get(url)
    status_list = r.json()['data']
    return status_list


# Calculate word frequency. Just an example, prob should do td-idf. And other features.
def feature_most_frequent_five_words(status_list):
    word_frequency_counter = Counter()
    for status in status_list:
        msg = status['message']
        word_frequency_counter.update(filter(bool, re.split("[^a-zA-Z]", msg)))
    return word_frequency_counter.most_common(5)


def calc_status_features(userid):
    status_list = get_status_list(userid)
    print feature_most_frequent_five_words(status_list)


if len(sys.argv) != 2:
    print "Usage: python {0} <fb-user-id>".format(sys.argv[0])
    sys.exit(0)

calc_status_features(sys.argv[1])