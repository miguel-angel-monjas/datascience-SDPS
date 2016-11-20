#!/usr/bin/env python

from operator import itemgetter
import sys

current_sequence = None
sequence = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    sequence, count = line.split('\t', 1)

    if current_sequence != sequence:
        if current_sequence:
            # write result to STDOUT
	    print '%s'% (sequence)
	current_sequence = sequence

