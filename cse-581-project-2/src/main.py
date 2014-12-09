import time
import tweepy
import consumer
import access_token
import sqlite3
import sys

DETROIT_WOEID = "2391585"
FIVE_MINUTES_IN_SECONDS = 5 * 60

db_name = time.strftime("../db/%Y-%m-%d-%H-%M-%S.db")

con = sqlite3.connect(db_name)

con.execute(
'''
CREATE TABLE trend_results(
  inserted,
  contents
)
'''
)

con.execute(
'''
CREATE TABLE stream_results(
  inserted,
  contents
)
'''
)
con.commit()


def save(table, json, commit):
    values = (json,)
    sql = "INSERT INTO " + table + "(inserted,contents) VALUES(datetime('now'), ?)"

    con.execute(sql, values)

    if commit:
        con.commit()

start_time = 0


class StdOutListener(tweepy.StreamListener):

    def on_data(self, data):
        global start_time
        commit = time.time() - start_time > 60
        save("stream_results", data, commit)

        if commit:
            start_time = time.time()
            sys.stdout.write('S')
        else:
            sys.stdout.write('.')

        #if time.time() - start_time > 60:
        #    print
#       #     go()

        return True

    def on_error(self, status):
        print status


auth = tweepy.OAuthHandler(consumer.key, consumer.secret)
auth.set_access_token(access_token.key, access_token.secret)

api = tweepy.API(auth)
stream = tweepy.Stream(auth, StdOutListener())


def go():
    global start_time

    stream.disconnect()
    #result = api.trends_place(id=DETROIT_WOEID)
    #save("trend_results", result, True)
    #trends = result[0]["trends"]
    ##track = [str(trends[i]["name"]) for i in range(0, len(trends))]
    #print track

#    start_time = time.time()
    #stream.filter(locations=[-83.689438, 42.431179, -83.083393, 42.888647])
    '''stream.filter(languages=["en"], locations=[
            -83.551907, 42.02793, -82.74990799999999, 42.451336999999995,
            -84.158189, 42.423904, -83.664808, 42.783263,
            -83.102891, 42.447055, -82.70596599999999, 42.897541,
            -83.46074399999999, 42.880432, -82.98364699999999, 43.327048999999995,
            -82.996257, 42.477778, -82.33407299999999, 43.170412999999996,
            -83.689438, 42.431179, -83.083393, 42.888647])
    '''
    #stream.filter(languages=["en"], track=['iphone', 'ipad', 'ipod', 'imac'])
    stream.filter(languages=["en"], track=['nfl', 'nhl', 'nba'])
    #stream.filter(languages=["en"], track=['script'])

go()