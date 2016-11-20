#!/usr/bin/env python
import json
import sys

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
        tweet_country = tweet['place']['country_code']
        if tweet_lang == 'en' or tweet_lang == 'es':
            #print tweet_lang, tweet_country
            tweet_keys  = [tweet_lang, tweet_country]
            print ('%s\t1' % (tweet_keys))
    except Exception as e:
        #print type(e).__name__
        #print "No country code"
        continue

    #tweets_data.append(tweet)

#print len(tweets_data)