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
from datetime import datetime

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

reload(sys)
sys.setdefaultencoding('utf-8')
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
last_state = None
state_dict = {}
state = ''

# auxiliary variables for hashtag analysis
hashtag_bag = {}

tweet_score = 0

# input comes from STDIN
for line in sys.stdin:
    # capture lines
    line = line.strip()
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
        state, word = literal_eval(value)
        tweet_id = key

        # initialization
        if last_state is None:
            last_state = state

        if tweet_id != last_tweet:
            # first word in tweet: store previous tweet score and initialize counters
            last_tweet = tweet_id
            if state != last_state:
                # state change: flush data if needed
                if last_state not in state_dict:
                    state_dict[last_state] = []
                    state_dict[last_state].append(1)
                    state_dict[last_state].append(tweet_score)
                else:
                    state_dict[last_state][0] += 1
                    state_dict[last_state][1] += tweet_score
                last_state = state
            if word in afinn_dictionary:
                tweet_score = afinn_dictionary[word]
            else:
                tweet_score = 0
        else:
            # same tweet -> process as usual
            if word in afinn_dictionary:
                tweet_score += afinn_dictionary[word]
            else:
                continue

if reduce_operation == 'states':
    # store last tweet
    if last_state not in state_dict:
        state_dict[last_state] = []
        state_dict[last_state].append(1)
        state_dict[last_state].append(tweet_score)
    else:
        state_dict[last_state][0] += 1
        state_dict[last_state][1] += tweet_score

if reduce_operation == 'states':
    # print dictionary
    state_bag = [(v, k) for v, k in state_dict.iteritems()]
    state_bag.sort()
    for v, k in state_bag:
        print '%s;%d;%.2f' % (v, k[0], float(k[1]) / float(k[0]))
elif reduce_operation == 'hashtags':
    inverse_bag = [(v, k) for k, v in hashtag_bag.iteritems()]
    inverse_bag.sort(reverse=True)
    for v, k in inverse_bag[:10]:
        print "%s: %d" % (k[1:], v)

sys.stderr.write('%s\n' %(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
