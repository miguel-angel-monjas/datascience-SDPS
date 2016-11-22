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

# argument management
parser = argparse.ArgumentParser()
parser.add_argument("--type", help="type of reduce operation: states of hashtags")
args = parser.parse_args()
if args.type in ['states', 'hashtags']:
    reduce_operation = args.type
else:
    reduce_operation = 'states'

# some nice counters
last_state = None
total_score = 0.0
total_tweets = 0

# auxiliary variables for hashtag analysis
hashtag_bag = {}

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    # capture lines
    key, value = line.split('\t')
    key_tuple = literal_eval(key)
    if key_tuple[0] == 0:
        if reduce_operation == 'states':
            continue
        hashtag = key_tuple[1]
        if hashtag in hashtag_bag:
            hashtag_bag[hashtag] += 1
        else:
            hashtag_bag[hashtag] = 1
    elif key_tuple[0] == 1:
        if reduce_operation == 'hashtags':
            continue
        # capture values from mapper
        state = key_tuple[1]
        score = value
        # initialization
        if last_state is None:
            last_state = state
            total_score = float(score)
            total_tweets = 1
        # per tweet processing
        if state != last_state:
            # first tweet in state: flush previous state and initialize counters
            print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))
            last_state = state
            total_score = float(score)
            total_tweets = 1
        else:
            # remaining tweets in the same state
            total_score += float(score)
            total_tweets += 1
if reduce_operation == 'states':
    # flush final state
    print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))

if reduce_operation == 'hashtags':
    inverse_bag = [(v, k) for k, v in hashtag_bag.iteritems()]
    inverse_bag.sort(reverse=True)
    for v, k in inverse_bag[:10]:
        print "%s: %d" % (k, v)