#!/usr/bin/env python
import sys

dict_ = {} # initialize an empty dictionary

# Process each key-value pair from the mapper
for line in sys.stdin:
   line = line[:-1]
   # Get the key and value from the current line
   word, title = line.split('\t')
   title = title[:-4]
   #print(word)
   if word not in dict_:
       dict_[word] = [title]
   elif title not in dict_[word] :
       dict_[word].append(title)

for key in dict_ :
    string_dict = '"'+'", "'.join(dict_[key])+'"'
    print ("%s\t%s" % (key, string_dict))
