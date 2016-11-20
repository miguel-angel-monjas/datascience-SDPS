#!/usr/bin/env python

from operator import itemgetter
import sys

previous_friendship = None
friendship = None
count = 0

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    friendship, person = line.split('\t', 1)

    if previous_friendship == friendship:
        count = count + 1
    else:
        if count == 1:
            # write result to STDOUT
            print '%s'% (previous_friendship)
	count = 1
	previous_friendship = friendship 

# do not forget to output the last word if needed!
if count == 1:
    print '%s'% (previous_friendship)

