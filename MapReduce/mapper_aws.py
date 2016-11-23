#!/usr/bin/env python

"""Implements two mapper functions for the Tweeter feeling problem.

The first mapper function extracts the valid words from the tweet. The tweet id is used as key while the value is
a tuple containing the state and the actual word. The second mapper function provides an output for each hashtag. Key
is the hashtag, value is not relevant.

Adaptation to AWS EMR is done by using an S3 URL instead of a local file location.

"""

import json
import re
import sys
import urllib2

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

sys.path.append('.')

STATES_FILE_URL = 'https://s3-eu-west-1.amazonaws.com/urjc.datascience.mmonjas.emr/logic/us_states.txt'

# state file opening and dictionary population
states_dictionary = {}
f = urllib2.urlopen(STATES_FILE_URL)
for line in f:
    states_dictionary[line.split('\t')[0]] = line.strip().split('\t')[1]

# input processing
for line in sys.stdin:
    try:
        tweet = json.loads(line, encoding='latin-1')
        tweet_id = tweet["id_str"]
        tweet_text = tweet["text"]
        tweet_lang = tweet["lang"]
        tweet_place = tweet['place']
        if tweet_place is None:
            continue
    except Exception as e:
        #print type(e).__name__
        continue

    try:
        tweet_country = tweet_place['country_code']
        if tweet_country == 'US' and tweet_lang == 'en':
            location_tokens = tweet_place['full_name'].split(', ')
            if location_tokens[1] == 'USA':
                tweet_us_state = location_tokens[0]
            else:
                tweet_us_state = states_dictionary[location_tokens[1]]

            words = re.findall(r"[\w#]+", tweet_text)
            words = [word for word in words if (len(word) > 0)]
            for word in words:
                if word.startswith('#'):
                    print ('%s\t1' % (word))
                    word = word.replace('#','')
                elif '#' in word:
                    continue
                word = word.lower()
                map_value = [tweet_us_state, word]
                print ('%s\t%s' % (tweet_id, map_value))
    except Exception as e:
        #print type(e).__name__
        continue
