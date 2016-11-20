#!/usr/bin/env python

import sys
import json

# input comes from STDIN (standard input)
for dataline in sys.stdin:
    record = json.loads(dataline, encoding='latin-1')
    # key: document identifier
    # value: document contents
    matrix = record[0]
    i = record[1]
    j = record[2]
    value = record[3]
    if (matrix == "a"):
    	for k in range (0,5):
	      position = [i,k]
	      data = [str(matrix), j, value]
	      print '%s\t%s' % (position,data)
    elif (matrix == "b"):
    	for k in range (0,5):
	      position = [k,j]
	      data = [str(matrix), i, value]
	      print '%s\t%s' % (position,data)



