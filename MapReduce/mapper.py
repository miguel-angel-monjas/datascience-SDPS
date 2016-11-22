#!/usr/bin/env python

"""Implements two mapper functions for the Tweeter feeling problem.

The first mapper function computes the score for each tweet and provides an
output for each tweet. Key is the state and value the score.
The second mapper function provides an output for each hashtag. Key is the
hashtag, value is not relevant.
"""

import json
import os
import re
import sys

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

sys.path.append('.')

AFFIN_FILE = 'AFINN-111.txt'
STATES_FILE = 'us_states.txt'

# affinity file opening and dictionary population
afinn_dictionary = {}
f = open(AFFIN_FILE, 'r')
for line in f:
    afinn_dictionary[line.split('\t')[0]] = int(line.strip().split('\t')[1])
f.close()

# state file opening and dictionary population
states_dictionary = {}
f = open(STATES_FILE, 'r')
for line in f:
    states_dictionary[line.split('\t')[0]] = line.strip().split('\t')[1]
f.close()

# input processing
for line in sys.stdin:
    try:
        tweet = json.loads(line, encoding='latin-1')
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
            tweet_score = 0
            words = re.findall(r"[\w#]+", tweet_text)
            #print tweet_text
            words = [word for word in words if (len(word) > 0)]
            for word in words:
                if word.startswith('#'):
                    word = word.replace('#','')
                    hash_key = [0, word]
                    print ('%s\t1' % (hash_key))
                elif '#' in word:
                    continue
                word = word.lower()
                if word in afinn_dictionary:
                    tweet_score += afinn_dictionary[word]
            location_tokens = tweet_place['full_name'].split(', ')
            if location_tokens[1] == 'USA':
                tweet_us_state = location_tokens[0]
            else:
                tweet_us_state = states_dictionary[location_tokens[1]]
            affin_key = [1, tweet_us_state]
            print ('%s\t%d' % (affin_key, tweet_score))
    except Exception as e:
        #print type(e).__name__
        continue
