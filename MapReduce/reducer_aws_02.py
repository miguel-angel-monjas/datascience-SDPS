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
    # capture lines
    line = line.strip()
    state, value = line.split('\t')
    tweet_count, state_score = literal_eval(value)

    if state in state_dict:
        state_dict[state][1] = (state_dict[state][0]*state_dict[state][1]+tweet_count*state_score) / \
                               (state_dict[state][0]+state_score)
        state_dict[state][0] = + tweet_count
    else :
        state_dict[state] = []
        state_dict[state].append(tweet_count)
        state_dict[state].append(state_score)

for item in state_dict :
    print ('%s;%d;%.2f' %(item, state_dict[item][0], state_dict[item][1]))