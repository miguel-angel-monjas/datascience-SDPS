#!/usr/bin/env python

"""


"""

import sys
from ast import literal_eval

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

state_dict = {}

# input comes from STDIN
for line in sys.stdin:
    # capture lines and obtain input data: state, tweet count and state score
    try:
        line = line.strip()
        state, value = line.split('\t')
        tweet_count, state_score = literal_eval(value)
    except:
        continue

    if state not in state_dict:
        state_dict[state] = []
        state_dict[state].append(tweet_count)
        state_dict[state].append(state_score)
    else:
        state_dict[state][1] = (state_dict[state][0]*state_dict[state][1]+tweet_count*state_score) / \
                               (state_dict[state][0]+tweet_count)
        state_dict[state][0] += tweet_count

state_bag = [(v, k) for v, k in state_dict.iteritems()]
state_bag.sort()
for v, k in state_bag:
    print '%s;%d;%.2f' % (v, k[0], k[1])
