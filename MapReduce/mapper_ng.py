#!/usr/bin/env python

import json
#import us
#from us_states import states
import os
import re
import sys

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'FM': 'Micronesia',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MH': 'Marshall Islands',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'PW': 'Palau',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

sys.path.append('.')

pathname = os.path.join(os.getcwd(), 'AFINN-111.txt')
dictionary = {}

f = open('AFINN-111.txt', 'r')
for line in f:
    dictionary[line.split('\t')[0]] = int(line.strip().split('\t')[1])
f.close()
#print dictionary

for line in sys.stdin:
    try:
        tweet = json.loads(line, encoding='latin-1')
        tweet_text = tweet["text"]
        tweet_lang = tweet["lang"]
        tweet_place = tweet['place']
        if tweet_place == None :
            continue
    except Exception as e:
        continue
    try:
        #print line
        #print tweet_place
        #raw_input('>')
        tweet_country = tweet_place['country_code']
        if tweet_country == 'US' and tweet_lang == 'en':
            #print tweet_text
            tweet_score = 0
            words = re.findall(r"[\w']+|", tweet_text)
            words = [word.lower() for word in words if (len(word) > 0)]
            for word in words :
                if word in dictionary:
                    tweet_score += dictionary[word]
            location_tokens = tweet_place['full_name'].split(', ')
            if location_tokens[1] == 'USA' :
                tweet_us_state = location_tokens[0]
            else :
                tweet_us_state = states[location_tokens[1]]
                #tweet_us_state = us.states.lookup(location_tokens[1]).name
            print ('%s\t%d' % (tweet_us_state, tweet_score))
    except Exception as e:
        #print type(e).__name__
        #print "No country code"
        continue

    #tweets_data.append(tweet)

#print len(tweets_data)