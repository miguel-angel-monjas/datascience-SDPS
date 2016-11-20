#!/usr/bin/env python

import sys
import ast

# input comes from STDIN

last_state = None
total_score = 0.0
total_tweets = 0
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
    # first tweet in state
    if state != last_state :
        print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))
        last_state = state
        total_score = float(score)
    else :
        total_score += float(score)
        total_tweets += 1
print '%s;%d;%.2f' %(last_state, total_tweets, total_score/float(total_tweets))
