#!/usr/bin/env python

"""


"""

import argparse
import sys
from ast import literal_eval

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

# some nice counters
last_state = None
tweet_score = 0
tweet_counter = 0

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    # capture lines
    state, score = line.split('\t')

    # initialization
    if last_state is None:
        last_state = state

    if state != last_state:
        # state change: flush data if needed
        print('%s;%s' %(last_state, tweet_score))
        print '%s;%d;%.2f' % (last_state, tweet_counter, float(tweet_score) / float(tweet_counter))
        last_state = state
        tweet_score = 0
        tweet_counter = 0
    else :
        tweet_score += int(score)
        tweet_counter += 1
# store last tweet
print '%s;%d;%.2f' % (last_state, tweet_counter, float(tweet_score) / float(tweet_counter))
