import os
import sys
import time
import logging
import sqlite3


class TweetRepository:

    def __init__(self, config):
        self.db_path = None
        self.con = None
        self.last_commit = None

        self.data_folder = config.data_folder()
        self.commit_seconds = config.commit_seconds()
        self.db_size_limit = config.db_size_limit()

        self._create_database()

    def _create_database(self):

        self.db_path = os.path.join(self.data_folder, time.strftime("%Y-%m-%d-%H-%M-%S.db"))

        self.con = sqlite3.connect(self.db_path)
        self.con.execute("CREATE TABLE tweets(tweet)")
        self.con.commit()
        self.last_commit = time.time()

        logging.info("Database created: {0}".format(self.db_path))

    def add(self, tweet):

        values = (tweet,)
        sql = "INSERT INTO tweets(tweet) VALUES(?)"
        self.con.execute(sql, values)

        db_size = os.stat(self.db_path).st_size
        if db_size > self.db_size_limit:
            self.close()
            self._create_database()
        elif time.time() > self.last_commit + self.commit_seconds:
            self._commit()
            sys.stdout.write("c")
        else:
            sys.stdout.write(".")
        sys.stdout.flush()

    def _commit(self):
        self.con.commit()
        self.last_commit = time.time()

    def close(self):
        self.con.commit()
        self.con.close()