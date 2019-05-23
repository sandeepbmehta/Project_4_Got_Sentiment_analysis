import tweepy as tw
import pandas as pd
import requests
import json
from textblob import TextBlob
import re
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from bs4 import BeautifulSoup
import requests
import pprint
import pymongo
from sqlalchemy import func
from nltk.stem import WordNetLemmatizer

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
access_token = "1126320149202472963-WFvSDnYa1eL6osrEorVskuxFLAsoZB"
access_token_secret = "tYUy2yIjqPGtBYPxVUGwNl71rnFqErsMXCM05nAFphvUf"
consumer_key = "svHJE3Vx9Yo6IIxGRoCtZwkK5"
consumer_secret = "pmMPOP6ccTWxl675HCprsTyKnyQzWK6Vz9ZupnBSTp2uehVH73"

master_list = (["#NotToday", 
              "#TheLongNight.", 
              "#GameofThrones",  
              "#Dracarys",  
              "#GOT", 
              "#GOTS8", 
              "#ForTheThrone", 
              "#DaenerysTargaryen", 
              "#JonSnow", 
              "#NightKing", 
              "#CerseiLannister", 
              "#AryaStark", 
              "#JaimeLannister", 
              "#TyrionLannister", 
              "#SansaStark",
              "#BranStark", 
              "#BrienneOfTarth", 
              "#DavosSeaworth", 
              "#EuronGreyjoy", 
              "#JorahMormont", 
              "#Greyworm", 
              "#Melisandre", 
              "#Missandei", 
              "#SamwellTarly", 
              "#TheonGreyjoy", 
              "#Varys", 
              "#TheHound"
             ])
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

search_words = '#JonSnow OR "Jon Snow"'
char_name = "Jonsnow"

dates = [["2019-05-11", "2019-05-12"], 
         ["2019-05-12", "2019-05-13"], 
         ["2019-05-13", "2019-05-14"], 
         ["2019-05-14", "2019-05-15"],
         ["2019-05-15", "2019-05-16"],
         ["2019-05-16", "2019-05-17"],
         ["2019-05-17", "2019-05-18"]
        ]

date_since = ""
date_until = ""
tweet_text = []
tweet_timestamp = []
tweet_date = []
tweet_char = []
tweet_sen = []
tweet_pol = []
tweet_sub = []

for date_list in dates:
    date_since = date_list[0]
    date_until = date_list[1]
    tweets = tw.Cursor(api.search,
            q=search_words,
            lang="en",
            since=date_since, until=date_until, encode="utf-8").items(100)
    
    for tweet in tweets:
        tweet_date.append(tweet.created_at.strftime('%m/%d/%Y'))
        tweet_timestamp.append(tweet.created_at.strftime('%m/%d/%Y %H:%M:%S'))
    
        analysis = TextBlob(tweet.text)

        senti = ""
        polarity = 0.0
        subjectivity = 0.0
    
        if analysis.sentiment[0]>0:
           senti = "Pos"
        elif analysis.sentiment[0]<0:
           senti = "Neg"
        else:
           senti = "Neu"
    
        polarity = float(analysis.sentiment[0])
        subjectivity = float(analysis.sentiment[1])

        tweet_text.append(tweet.text)
        tweet_char.append(char_name)
        tweet_pol.append(polarity)
        tweet_sen.append(senti)
        tweet_sub.append(subjectivity)

df = pd.DataFrame({
  "text": tweet_text,
  "date" : tweet_date,
  "char" : tweet_char,
  "sentiment" : tweet_sen,
  "polarity" : tweet_pol,
  "subjectivity" : tweet_sub,
  "timestamp" : tweet_timestamp
})

df = df.dropna()
stemmer = WordNetLemmatizer()

for index, row in df.iterrows():
    # Remove all the special characters
    test_preproc = re.sub(r'\W', ' ', str(row["text"]))

    # remove all single characters
    test_preproc = re.sub(r'\s+[a-zA-Z]\s+', ' ', test_preproc)

    # Remove single characters from the start
    test_preproc = re.sub(r'\^[a-zA-Z]\s+', ' ', test_preproc) 

    # Substituting multiple spaces with single space
    test_preproc = re.sub(r'\s+', ' ', test_preproc, flags=re.I)

    # Removing prefixed 'b'
    test_preproc = re.sub(r'^b\s+', '', test_preproc)

    # Converting to Lowercase
    test_preproc = test_preproc.lower()
    
    # Lemmatization
    test_preproc = test_preproc.split()

    test_preproc = [stemmer.lemmatize(word) for word in test_preproc]
    comb_string = ' '.join(test_preproc)
    df.loc[index, "Preprocess"] = comb_string

df.to_csv("data/Jonsnow_11_18.csv", index=False)