#!/usr/bin/env python
import sys

curr_code = None
code_counter = 0

# Process each key-value pair from the mapper
for line in sys.stdin:
   line = line[:-1]
   # Get the key and value from the current line
   code, count = line.split('\t')
   #print(code)

   if code != curr_code :
       if curr_code:
           code_counter += 1
           print ("%d->%s" %(code_counter, curr_code))
       curr_code = code

# Output the count for the last code
if curr_code == code:
   code_counter += 1
   print ("%d->%s" %(code_counter, curr_code))