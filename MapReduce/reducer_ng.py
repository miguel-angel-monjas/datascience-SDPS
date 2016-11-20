#!/usr/bin/env python

import sys
import ast

# input comes from STDIN

last_state = None
total_score = 0
total_tweets = 0
for line in sys.stdin:
    line = line.strip()
    #print line
    # capture values from mapper
    state, score = line.split('\t')
    # initial
    if last_state == None :
        last_state = state
        total_score = score

    if state != last_state :
        print '%s -> %d' %(last_state, total_score)
        last_state = state
        total_score = score
    else :
        total_score += score
print '%s -> %d' %(last_state, total_score)
