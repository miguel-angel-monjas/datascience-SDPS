#!/usr/bin/env python

"""Provides two reducer functions for the Tweeter feeling problem.

The first reducer function takes the output of the mapper function and
determines the average per-state Tweeter feeling. The output is a CSV
structure.
The second reducer function determines the ten most popular hashtags.
The output is also a CSV structure.
Reducer selection is made by means of the --type argument
"""

import argparse
import sys
from ast import literal_eval

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

sys.path.append('.')

AFFIN_FILE = 'AFINN-111.txt'

# argument management
parser = argparse.ArgumentParser()
parser.add_argument("--type", help="type of reduce operation: states of hashtags")
args = parser.parse_args()
if args.type in ['states', 'hashtags']:
    reduce_operation = args.type
else:
    reduce_operation = 'states'

# affinity file opening and dictionary population
afinn_dictionary = {}
f = open(AFFIN_FILE, 'r')
for line in f:
    afinn_dictionary[line.split('\t')[0]] = int(line.strip().split('\t')[1])
f.close()

# some nice counters
last_tweet = None
state_dict = {}
state = ''

# auxiliary variables for hashtag analysis
hashtag_bag = {}

tweet_score = 0

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    # capture lines
    key, value = line.split('\t')
    if key.startswith('#'):
        if reduce_operation == 'states':
            continue
        hashtag = key
        if hashtag in hashtag_bag:
            hashtag_bag[hashtag] += 1
        else:
            hashtag_bag[hashtag] = 1
    else:
        if reduce_operation == 'hashtags':
            continue

        # capture values from mapper
        mapper_tuple = literal_eval(value)
        state = mapper_tuple[0]
        word = mapper_tuple[1]
        tweet_id = key

        # initialization
        if last_tweet is None:
            last_tweet = tweet_id

        if tweet_id != last_tweet:
            # first word in tweet: store previous tweet score and initialize counters
            if state not in state_dict and tweet_score > 0:
                state_dict[state] = []
                state_dict[state].append(1)
                state_dict[state].append(tweet_score)
            elif tweet_score > 0:
                state_dict[state][0] += 1
                state_dict[state][1] += tweet_score
            last_tweet = tweet_id
            if word in afinn_dictionary:
                tweet_score = afinn_dictionary[word]
            else:
                tweet_score = 0
                continue
        else:
        # remaining words in the same tweet
            if word in afinn_dictionary:
                tweet_score += afinn_dictionary[word]
            else:
                continue

if reduce_operation == 'states':
    # store last tweet
    if state not in state_dict and tweet_score > 0:
        state_dict[state] = []
        state_dict[state].append(1)
        state_dict[state].append(tweet_score)
    elif tweet_score > 0:
        state_dict[state][0] += 1
        state_dict[state][1] += tweet_score
    # print dictionary
    state_bag = [(v, k) for v, k in state_dict.iteritems()]
    state_bag.sort()
    for v, k in state_bag:
        print '%s;%d;%.2f' % (v, k[0], float(k[1]) / float(k[0]))

if reduce_operation == 'hashtags':
    inverse_bag = [(v, k) for k, v in hashtag_bag.iteritems()]
    inverse_bag.sort(reverse=True)
    for v, k in inverse_bag[:10]:
        print "%s: %d" % (k[1:], v)