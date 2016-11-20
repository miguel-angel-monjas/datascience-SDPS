#!/usr/bin/env python
import sys

current_friend = None
dict_of_friends = {}

# Process each key-value pair from the mapper
for line in sys.stdin:
   line = line[:-1]
   # Get the key and value from the current line
   friend_a, friend_b = line.split('\t')

   if friend_a not in dict_of_friends :
       dict_of_friends[friend_a] = []
       #print('+++   Creo ', friend_a)

   if friend_b in dict_of_friends and friend_a in dict_of_friends[friend_b] :
       #print('Remove %s from %s' %(friend_a, friend_b))
       dict_of_friends[friend_b].remove(friend_a)
   else :
       #print('Add %s to %s' %(friend_b, friend_a))
       dict_of_friends[friend_a].append(friend_b)

#print(dict_of_friends)
for key in dict_of_friends :
    for item in dict_of_friends[key] :
       print ("%s\t%s" % (item, key))
