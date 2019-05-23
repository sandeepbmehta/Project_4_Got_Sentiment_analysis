from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from bs4 import BeautifulSoup
import requests
import pprint
import json
import pymongo
from sqlalchemy import func

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
# Define the 'classDB' database in Mongo
db = client.projDB
# tweet = db.char_hashtags.find()

#Variables that contains the user credentials to access Twitter API
access_token = "114010579-UscavtyluJ4ZOjGBGPwF3Xy8i5ynDgmeiYRLQ9WL"
access_token_secret = "hnA5I14kCwovdQF1Ciyz3VWOJlPlre8jHEKoeb9OshhJe"
consumer_key = "j2BhP2Q3LFCzpPQ5o0Xx4GuY7"
consumer_secret = "vkcmHL1U71cpqdn1LBl7GY4cdJIkvFotKAyZeChIuHBoq5aQ2j"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
   def on_data(self, data):
    # Insert a document into the 'tweet' collection
        data = json.loads(data)
        if data["lang"] == 'en':
            db.char_hashtags.insert_one(
                {
                'id': int(data["id"]),
                'text': data["text"],
                'language': data["lang"],
                'created': data["created_at"],
                'entities' : data["entities"],
                'place' : data["place"],
                'source' : data["source"]
                })
#         print(data)
        return True

   def on_error(self, status):
       print(status)


#This handles Twitter authetification and the connection to Twitter Streaming API
l = StdOutListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, l)

#This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
stream.filter(track=['DaenerysTargaryen', '#DaenerysTargaryen'])
# stream.filter(track=['Game of Thrones', 'A Song of Ice and Fire', 'Iron Thrones'])
# start_mining(["#NotToday", 
#               "#TheLongNight.", 
#               "#GameofThrones",       Complete
#               "#Dracarys",            Complete
#               "#GOT", 
#               "#GOTS8", 
#               "#ForTheThrone", 
#               "#DaenerysTargaryen",   In Progress
#               "#JonSnow", 
#               "#NightKing", 
#               "#CerseiLannister", 
#               "#AryaStark", 
#               "#JaimeLannister", 
#               "#TyrionLannister", 
#               "#SansaStark",
#               "#BranStark", 
#               "#BrienneOfTarth", 
#               "#DavosSeaworth", 
#               "#EuronGreyjoy", 
#               "#JorahMormont", 
#               "#Greyworm", 
#               "#Melisandre", 
#               "#Missandei", 
#               "#SamwellTarly", 
#               "#TheonGreyjoy", 
#               "#Varys", 
#               "#TheHound"
#              ])