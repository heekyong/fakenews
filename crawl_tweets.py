import tweepy
import os
import sys
import pandas as pd
import numpy as np
import pickle

# twiter api configuration
consumer_key = 
consumer_secret =
access_token =
access_token_secret =
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# load true/false tweet ids from csv
df = pd.read_csv('data_finals.csv')
true_list=[]
false_list=[]

for i in range(df.shape[0]):
    if(df.iloc[i,1]==0):
        true_list.append(df.iloc[i,0])
    else:
        false_list.append(df.iloc[i,0])

# crawl the tweets according to the ids
true_tweets=[]
false_tweets=[]

for i,tweet in enumerate(true_list):
    try:
        true_tweets.append(api.get_status(true_list[i]))
    except:
        pass
    print(i)

for i,tweet in enumerate(false_list):
    try:
        false_tweets.append(api.get_status(false_list[i]))
    except:
        pass
    print(i)

# save
with open('true.p', 'wb') as f:
    pickle.dump(true_tweets, f, pickle.HIGHEST_PROTOCOL)
with open('false.p', 'wb') as f:
    pickle.dump(false_tweets, f, pickle.HIGHEST_PROTOCOL)
