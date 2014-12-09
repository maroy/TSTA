import os
import sys
import glob
import json
import sqlite3
import datetime
import dateutil.parser

utc_epoch = datetime.datetime(1970,1,1,tzinfo=dateutil.tz.tzutc())

def to_utc_timestamp(str_date):
    dt = dateutil.parser.parse(str_date)
    return (dt - utc_epoch).total_seconds()


class Tweet:

    def __init__(self, db, id, tweet_dict):
        self.db = db
        self.id = id
        self.created = tweet_dict["created_at"]
        self.utc_timestamp = to_utc_timestamp(self.created)
        self.screen_name = tweet_dict["user"]["screen_name"]
        self.content = tweet_dict["text"]

        self.coordinates = ",".join([str(f) for f in tweet_dict["coordinates"]["coordinates"]]) if tweet_dict["coordinates"] is not None else None
        self.place = tweet_dict["place"]["full_name"] if tweet_dict["place"] is not None else None
        self.retweet = tweet_dict["retweeted"]


def create_index_database(path):
    con = sqlite3.connect(path)
    con.execute("CREATE TABLE tweets(db, id, created, utc_timestamp, screen_name, content, coordinates, place, retweet)")
    con.execute("CREATE UNIQUE INDEX unq ON tweets(db, id)");
    con.execute("CREATE INDEX scrn ON tweets(screen_name)")
    con.execute("CREATE INDEX ts ON tweets(utc_timestamp)")
    con.close()

def read_tweets(path):
    tweets = []
    con = sqlite3.connect(path)
    cur = con.cursor()
    sql = "SELECT _rowid_, tweet FROM tweets"
    file_name = os.path.basename(path)
    for row in cur.execute(sql):
        id = int(row[0])
        tweet_dict = json.loads(str(row[1]))
        tweet = Tweet(file_name,id,tweet_dict)
        tweets.append(tweet)
    con.close()
    return tweets

def save_tweets(path, tweets):
    idx_con = sqlite3.connect(path)

    sql = "INSERT INTO tweets(db, id, created, utc_timestamp, screen_name, content, coordinates, place, retweet) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    idx_con.executemany(
        sql,
        [(t.db, t.id, t.created, t.utc_timestamp, t.screen_name, t.content, t.coordinates, t.place, t.retweet) for t in tweets]
    )
    idx_con.commit()

    idx_con.close()

def get_indexed_dbnames(idx_db_path):
    db_names = []
    if os.path.isfile(idx_db_path):
        con = sqlite3.connect(idx_db_path)
        cur = con.cursor()
        sql = "SELECT DISTINCT db FROM tweets"
        for row in cur.execute(sql):
            db_names.append(row[0])
        con.close()
    return db_names

def main():
    folder = sys.argv[1]

    in_dbs = []
    pattern = os.path.join(folder, "*.db")
    for db_file in glob.glob(pattern):
        if not db_file.endswith("idx.db") and not db_file.endswith("idx2.db"):
            in_dbs.append(os.path.basename(db_file))

    idx_db_path = os.path.join(folder, "idx2.db")

    indexed_dbnames = get_indexed_dbnames(idx_db_path)

    for db_name in indexed_dbnames:
        if db_name in in_dbs:
            in_dbs.remove(db_name)

    if len(in_dbs) == 0:
        print "all dbs indexed"
        exit()

    if not os.path.isfile(idx_db_path):
        create_index_database(idx_db_path)

    for in_db in in_dbs:
        print "reading tweets from {0}".format(in_db)
        tweets = read_tweets(os.path.join(folder, in_db))
        print "    read {0} tweets".format(len(tweets))
        save_tweets(idx_db_path, tweets)
        print "    saved to index"


if __name__ == "__main__":
    main()