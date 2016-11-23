#!/usr/bin/env python

import json
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
        tweet_country = tweet_place['country_code']
        if tweet_country == 'US' and tweet_lang == 'en':
            location_tokens = tweet_place['full_name'].split(', ')
            if location_tokens[1] == 'USA' :
                print '%s\t1' %(location_tokens[0])
            else :
                print '%s\t1' %(states[location_tokens[1]])
    except Exception as e:
        #print type(e).__name__
        continue

    #tweets_data.append(tweet)

#print len(tweets_data)
