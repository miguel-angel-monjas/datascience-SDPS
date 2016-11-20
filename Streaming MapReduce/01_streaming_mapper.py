#!/usr/bin/env python

import sys
import json

trailing_dna = []

# Read each line from STDIN
for line in sys.stdin:
    record = json.loads(line)

    print ('%s\t1' %(record[1].strip()[:10]))