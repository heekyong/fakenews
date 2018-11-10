from pymongo import MongoClient
from collections import defaultdict
from collections import Counter
import numpy as np
import pandas as pd
import datetime
import re

import warnings
import pickle
warnings.filterwarnings('ignore')

client = MongoClient('server', 'port')
db = client['fakenews']
users_collection = db['users']
tweets_collection = db['tweets']

true_users = open("uploads/true_usernames.prn","r")
t_user_list=[]
for line in true_users:
    t_user_list.append(line.strip('\n'))

false_users = open("uploads/false_usernames.prn",'r')
f_user_list=[]
for line in false_users:
    f_user_list.append(line.strip('\n'))

users_cur = users_collection.find( { "$and" : [{"name": {"$in":t_user_list }}, {"verified":True}]} , {"name":1, "id":1,"_id":0})
true_users_id=[]
count =0
for user in users_cur:
    print(user)
    true_users_id.append(user['id'])
    count+=1
print(count)

users_cur = users_collection.find( { "name": {"$in":f_user_list }} , {"name":1, "id":1,"_id":0})
false_users_id=[]
count =0

for user in users_cur:
    print(user)
    false_users_id.append(user['id'])
    count+=1
print(count)

for user in true_users_id:
    tweetno=[]
    retweets = tweets_collection.find({'user.id':user}, {'id','created_at'})
    for tweets in retweets:
        count+=1
        #print(tweets)
        tweetno.append(tweets['id'])
        #print(count)

    # 각 오리지널 트윗의 리트윗들을 찾아서 리트윗 시점 수집
    retweets = defaultdict(list)

    for ids in tweetno:
        cur = tweets_collection.find({'retweeted_status.id':ids})
        for items in cur:
            #print(items['text'])
            retweets[ids].append(items['created_at'])

# 왜인지 모르겠지만 key에 'tweets'로 빈거 마지막에 하나 껴서 지워주기
#del npr_retweets['tweets']

# 시작날짜와 끝날짜 설정
    starting_date = datetime.date(year=2017, month=10, day=25).toordinal()
    ending_date = datetime.date(year=2018, month=1, day=16).toordinal()
    user_total_counts = defaultdict(int)


#npr의 각 오리지널 트윗별로
    for tweets in retweets:
        date_counts=defaultdict(int)
    #그 각 트윗의 리트윗 시점에 대해 날짜별 리트윗 수 카운트
        for day in range(starting_date,ending_date):

            for dates in retweets[tweets]:
                if(dates.toordinal() == day):
                    date_counts[str(day)]+= 1
                else:
                    pass
            #print(tweets, date_counts[str(day)])
        # 트윗별의 날짜별 트윗총합을 이제 유저계정 전체의 리트윗카운트로
            user_total_counts[str(day)] += date_counts[str(day)]

# 계정의 날짜별 리트윗수 총합인 user_total_counts (dict형)을 matrix로 변환하여 csv로 출력
    matrix = pd.DataFrame(user_total_counts, index=[0])
    matrix.T.to_csv(str(user)+'.csv', index=False, header=False)
