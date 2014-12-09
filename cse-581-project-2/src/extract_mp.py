import os
import time
import Queue
import random
import multiprocessing
import re
import sqlite3
import datetime
import HTMLParser

import nltk
import mysql.connector

idx_db_path = "../data/idx.db"
query = '''
SELECT
    db,
    id
    datetime(utc_timestamp, 'unixepoch', 'localtime') created,
    content
FROM
    tweets
ORDER BY
    utc_timestamp
'''
class KeywordExtractor:

    def __init__(self):
        self.html_parser = HTMLParser.HTMLParser()

        self.stop = nltk.corpus.stopwords.words("english")
        self.stop.append('rt')

        with open('contractions.txt', 'rb') as f:
            contractions = [c.strip() for c in f.readlines()]

        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
        self.tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

        self.url_regex = re.compile(r"http[s]?[^\s]*")
        self.contractions_regex = re.compile("|".join(contractions))

    def extract(self, source):
        text = source
        text = self.html_parser.unescape(text)
        text = text.lower()

        text = self.url_regex.sub('', text)
        text = self.contractions_regex.sub('', text)

        tokens = []
        for token in self.tokenizer.tokenize(text):
            token = self.lemmatizer.lemmatize(token)
            if token not in self.stop:
                tokens.append(token)

        items = [token.encode('utf8') for token in tokens]
        return " ".join(items)


def process_range(start, end):
    pass


def init_db():
    idx_db = sqlite3.connect('../data/idx.db')
    idx_db_cur = idx_db.cursor()

    tools_tb = mysql.connector.connect(host='192.168.56.101', db='project_two', user='tools', passwd='password')
    tools_tb_cur = tools_tb.cursor()

    '''
    idx_db_cur.execute('select distinct db from tweets')
    for row in idx_db_cur:
        tools_tb_cur.execute('INSERT INTO source_db(name) VALUES(%s)', (row[0],))
        print row
    tools_tb.commit()
    '''


    tools_tb_cur.close()
    tools_tb.close()

    idx_db_cur.close()
    idx_db.close()


def process_print(l,msg):
    with l:
        print "{0}: {1}".format(os.getpid(), msg)


def worker(q,l):
    process_print(l, "worker started.")

    while True:
        try:
            x = q.get(False)
            time.sleep(random.random())
            process_print(l, "got: " + str(x))
        except Queue.Empty:
            process_print(l, "worker done.")
            break


def main():
    q = multiprocessing.Queue()
    l = multiprocessing.Lock()

    process_print('startup: ' + str(datetime.datetime.now()))

    init_db()
    process_print('init_db complete')

    for i in range(5,30):
        q.put(i)

    processes = []
    for i in range(0,6):
        p = multiprocessing.Process(target = worker, args = (q,l))
        p.daemon = True
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    process_print('finished: ' + str(datetime.datetime.now()))

if __name__ == "__main__":
    main()


if __name__ == "__main__":

    init_db()
