#!/usr/bin/env python

from operator import itemgetter
import sys

current_word = None
word = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    word, book = line.split('\t', 1)

    if current_word == word:
   	if not(dict.has_key(book)):
      		dict[book] = 1.0
    else:
        if current_word:
            # write result to STDOUT
	    print '%s\t%s'% (current_word, dict.keys())
	dict = {} # initialize an empty dictionary
    	dict[book] = 1.0
        current_word = word


# do not forget to output the last word if needed!
if current_word == word:
    print '%s\t%s'% (word, dict.keys())

