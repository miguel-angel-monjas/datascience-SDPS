#!/usr/bin/env python

# coding: utf-8

import json
import sys
import re
from mrjob.job import MRJob
from mrjob.step import MRStep
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

__author__ = "Miguel-Angel Monjas"
__copyright__ = "Copyright 2016"
__license__ = "Apache 2.0"

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('.')

def length_and_sum(iterable):
    i = 0
    total = 0
    for item in iterable :
        i += 1
        total += item
    return i, total

class MRWordFrequencyCount(MRJob) :
    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer)
        ]


    def mapper (self, _, line) :
        STATES_FILE = 'us_states.txt'

        # state file opening and dictionary population
        states_dictionary = {}
        f = open(STATES_FILE, 'r')
        for file_line in f:
            states_dictionary[file_line.split('\t')[0]] = file_line.strip().split('\t')[1]
        f.close()
        try:
            tweet = json.loads(line, encoding='latin-1')
            tweet_id = tweet["id_str"]
            tweet_text = tweet["text"]
            tweet_lang = tweet["lang"]
            tweet_place = tweet['place']
            if tweet_place is None:
                return
        except Exception as e:
            #print type(e).__name__
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
                        word = word.replace('#', '')
                    word = word.lower()
                    yield (tweet_id, (tweet_us_state, word))
        except Exception as e:
            # print type(e).__name__
            return

    def combiner(self, tweet_id, state_and_word):
        AFFIN_FILE = 'AFINN-111.txt'

        # affinity file opening and dictionary population
        afinn_dictionary = {}
        f = open(AFFIN_FILE, 'r')
        for file_line in f:
            afinn_dictionary[file_line.split('\t')[0]] = int(file_line.strip().split('\t')[1])
        f.close()

        state_dict = {}
        for [state, word] in state_and_word:
            tweet_score = 0
            if word in afinn_dictionary:
                tweet_score = afinn_dictionary[word]

            if state not in state_dict:
                state_dict[state] = tweet_score
            else:
                state_dict[state] += tweet_score
        for state, score in state_dict.iteritems() :
            yield(state, score)


    def reducer(self, state, score):
        num_tweets, total_score = length_and_sum(score)
        yield (state, (float(num_tweets), round(float(total_score)/float(num_tweets), 2)))

if __name__ == '__main__' :
    MRWordFrequencyCount.run()
