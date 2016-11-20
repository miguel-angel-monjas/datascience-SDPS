#!/usr/bin/env python

import sys

last_state = None
total_score = 0.0
total_tweets = 0

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()
    #print line
    # capture values from mapper
    state, score = line.split('\t')
    # initialization
    if last_state == None :
        last_state = state
        total_score = float(score)
        total_tweets = 1
    # per tweet processing
    if state != last_state :
        # first tweet in state: flush previous state and initialize counters
        print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))
        last_state = state
        total_score = float(score)
        total_tweets = 1
    else :
        # remaining tweets in the same state
        total_score += float(score)
        total_tweets += 1
# flush final state
print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))
