#!/usr/bin/env python

from operator import itemgetter
import sys
import ast


current_position = None
position = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    position, data = line.split('\t', 1)

    if current_position == position:
	data = ast.literal_eval(data)
  	if (data[0] == "a"):
    	   a[data[1]] = data[2]
    	elif (data[0] == "b"):
    	   b[data[1]] = data[2]
    else:
        if current_position:
            # write result to STDOUT
	    for j in range(0,5):
    		total += a[j]*b[j]
    
    	    if total <> 0:
	        print '%s\t%s'% (current_position, total)
	total = 0
    	a = [0,0,0,0,0]
    	b = [0,0,0,0,0]

        current_position = position

	data = ast.literal_eval(data)
  	if (data[0] == "a"):
    	   a[data[1]] = data[2]
    	elif (data[0] == "b"):
    	   b[data[1]] = data[2]

if current_position == position:
   # write result to STDOUT
   for j in range(0,5):
	total += a[j]*b[j]
    
   if total <> 0:
        print '%s\t%s'% (current_position, total)


    
