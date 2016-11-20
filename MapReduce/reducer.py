#!/usr/bin/env python

import sys
import ast

# input comes from STDIN
matrix = {'es': {}, 'en': {}}

for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()
    lang_and_loc = ast.literal_eval(line.split('\t')[0])
    lang = lang_and_loc[0]
    loc = lang_and_loc[1]
    if loc in matrix[lang] :
        matrix[lang][loc] += 1
    else :
        matrix[lang][loc] = 1

for country in matrix['es'] :
    print 'Spanish (%s) -> %d' %(country, matrix['es'][country])

for country in matrix['en'] :
    print 'English (%s) -> %d' %(country, matrix['en'][country])