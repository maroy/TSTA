import sys
import sqlite3

db = sqlite3.connect('../nfl_tweets.db')

keywords = {}
count = 0
for row in db.execute('SELECT keywords FROM nfl_tweets'):
    count += 1
    for keyword in row[0].split(' '):

        if keyword in keywords:
            keywords[keyword] += 1
        else:
            keywords[keyword] = 1

    if count % 10000 == 0:
        sys.stdout.write('.')
        sys.stdout.flush()

print len(keywords)
with open('../nfl_keywords.csv', 'wb') as f:
    for kw in sorted(keywords, lambda l, r: cmp(keywords[r], keywords[l])):
        f.write(kw.encode('utf8') + ',' + str(keywords[kw]) + '\n')
db.close