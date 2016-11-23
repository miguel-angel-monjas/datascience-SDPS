#!/usr/bin/env python

import sys

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

# some nice counters
state_dict = {}

# input comes from STDIN
for line in sys.stdin:
    line = line.strip()

    state, value = line.split('\t')

    if state not in state_dict:
        state_dict[state] = 1
    else:
        state_dict[state] += 1

# print dictionary
state_bag = [(v, k) for v, k in state_dict.iteritems()]
state_bag.sort()
for v, k in state_bag:
    print '%s;%d' % (v, k)