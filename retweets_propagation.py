from pymongo import MongoClient
from collections import defaultdict
from collections import Counter
import numpy as np
import pandas as pd
import re
import warnings
import datetime
import pickle
warnings.filterwarnings('ignore')

client = MongoClient('address', port)
db = client['fakenews']
users_collection = db['users']
tweets_collection = db['tweets']

# infowars 계정이 작성한 트윗들의 고유번호를 infowars_tweetno에 저장
infowars_tweetno = []
infowars = tweets_collection.find({'user.id':14505245}, {'id','created_at'})
count=0

for tweets in infowars:
    count+=1
    print(tweets)
    infowars_tweetno.append(tweets['id'])
    print(count)

# 각 오리지널 트윗의 리트윗들을 찾아서 리트윗 시점 수집
infowars_retweets = defaultdict(list)

for ids in infowars_tweetno:
    cur = tweets_collection.find({'retweeted_status.id':ids})
    for items in cur:
        print(items['text'])
        infowars_retweets[ids].append(items['created_at'])

# 왜인지 모르겠지만 key에 'tweets'로 빈거 마지막에 하나 껴서 지워주기
del infowars_retweets['tweets']

# 시작날짜와 끝날짜 설정
starting_date = datetime.date(year=2017, month=10, day=25).toordinal()
ending_date = datetime.date(year=2018, month=1, day=16).toordinal()
user_total_counts = defaultdict(int)


#infowars의 각 오리지널 트윗별로
for tweets in infowars_retweets:
    date_counts=defaultdict(int)
    #그 각 트윗의 리트윗 시점에 대해 날짜별 리트윗 수 카운트
    for day in range(starting_date,ending_date):

        for dates in infowars_retweets[tweets]:
            if(dates.toordinal() == day):
                date_counts[str(day)]+= 1
            else:
                pass
        print(tweets, date_counts[str(day)])
        # 트윗별의 날짜별 트윗총합을 이제 유저계정 전체의 리트윗카운트로
        user_total_counts[str(day)] += date_counts[str(day)]

# 계정의 날짜별 리트윗수 총합인 user_total_counts (dict형)을 matrix로 변환하여 csv로 출력
infowars_matrix = pd.DataFrame(user_total_counts, index=[0])
infowars_matrix.T.to_csv('infowars.csv', index=False, header=False)
