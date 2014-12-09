import re
import sqlite3
import datetime
import HTMLParser

import nltk

html_parser = HTMLParser.HTMLParser()

stop = nltk.corpus.stopwords.words("english")
stop.append('rt')
stop_words_regex = re.compile(r'\b' + r'\b|\b'.join(stop) + r'\b')

numbers_only_regex = re.compile(r'\b\d+\b')
whitespace_regex = re.compile(r'[\s]+')
url_regex = re.compile(r'http[s]?[^\s]*')
invalid_chars_regex = re.compile(r"[^a-z0-9 ]+")


with open('contractions.txt', 'rb') as f:
    contractions = [c.strip().lower() for c in f.readlines()]
contractions_regex = re.compile(r'\b' + r'\b|\b'.join(contractions) + r'\b')


db = sqlite3.connect("/Users/maroy/TWEETS/idx.db")

last_day = None
files = {}
count = 0;
for row in db.execute('SELECT utc_timestamp, content FROM tweets'):
    
    day = datetime.datetime.fromtimestamp(row[0]).strftime('%m-%d')
    
    if day != last_day:
        if day not in files:
            files[day] = []
        lines = files[day]

    content = row[1].lower()
    content = html_parser.unescape(content)
    content = url_regex.sub(' ', content)
    content = contractions_regex.sub(' ', content)
    content = stop_words_regex.sub(' ', content)
    content = invalid_chars_regex.sub(' ', content)
    content = numbers_only_regex.sub(' ', content)

    content = whitespace_regex.sub(' ', content).strip()

    lines.append("{0}: {1}".format(row[0], content))
    count += 1

    if count % 50000 == 0:
        print count

print count



for day in files:
    with open('text/day_' + str(day) + '.txt', 'wb') as f:
        f.write('\n'.join(files[day]))