#!/usr/bin/env python

# coding: utf-8

import json
import sys
import re
from mrjob.job import MRJob
from mrjob.step import MRStep


__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

sys.path.append('.')

STATES_FILE = 'us_states.txt'

# state file opening and dictionary population
states_dictionary = {}
f = open(STATES_FILE, 'r')
for line in f:
    states_dictionary[line.split('\t')[0]] = line.strip().split('\t')[1]
f.close()

class MRWordFrequencyCount(MRJob) :

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_files)
        ]

    def mapper (self, _, line) :
        try:
            tweet = json.loads(line, encoding='latin-1')
            tweet_id = tweet["id_str"]
            tweet_text = tweet["text"]
            tweet_lang = tweet["lang"]
            tweet_place = tweet['place']
            if tweet_place is None:
                return
        except Exception as e:
            # print type(e).__name__
            return

        try:
            tweet_country = tweet_place['country_code']
            if tweet_country == 'US' and tweet_lang == 'en':
                location_tokens = tweet_place['full_name'].split(', ')
                if location_tokens[1] == 'USA':
                    if location_tokens[0] in states_dictionary.values():
                        tweet_us_state = location_tokens[0]
                    else:
                        raise ValueError('Wrong state name')
                else:
                    tweet_us_state = states_dictionary[location_tokens[1]]

                words = re.findall(r"[\w#]+", tweet_text)
                words = [word for word in words if (len(word) > 0)]
                for word in words:
                    if word.startswith('#'):
                        yield (word, 1)
                        word = word.replace('#', '')
                    elif '#' in word:
                        continue
                    word = word.lower()
                    map_value = [tweet_us_state, word]
                    yield (tweet_id, map_value)
        except Exception as e:
            # print type(e).__name__
            return

if __name__ == '__main__' :
    MRWordFrequencyCount.run()
