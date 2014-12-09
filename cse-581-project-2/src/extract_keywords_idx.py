import re
import sys
import sqlite3
import datetime
import HTMLParser

import nltk

class OutputFiles:

    def __init__(self,limit):
        self.limit = limit

        self.nba = open('output/' + self.limit + ' nba.txt', 'w')
        self.nfl = open('output/' + self.limit + ' nfl.txt', 'w')
        self.nhl = open('output/' + self.limit + ' nhl.txt', 'w')
        self.any = open('output/' + self.limit + ' any.txt', 'w')

        self.cleanup_regex = re.compile(r'\bnba|nfl|nhl\b')

    def close(self):
        self.nba.close()
        self.nfl.close()
        self.nhl.close()
        self.any.close()

    def write(self, contents):
        nba = 'nba' in contents
        nfl = 'nfl' in contents
        nhl = 'nhl' in contents
        
        contents = self.cleanup_regex.sub('', contents) + '\n'

        if any([nba, nfl, nhl]):
            self.any.write(contents)

        if nba:
            self.nba.write(contents)

        if nfl:
            self.nfl.write(contents)

        if nhl:
            self.nhl.write(contents)


print 'startup: ' + str(datetime.datetime.now())

limits = []
for d in range(5,30):
    for h in range(0,24):
        for m in range(0,60,15):
            limits.append(unicode("2014-11-%02d %02d:%02d:00" % (d, h, m)))

limits = [limit for limit in limits if limit >= '2014-11-05 22:45:00']

query = '''
SELECT
    datetime(utc_timestamp, 'unixepoch', 'localtime') created,
    content
FROM
    tweets
ORDER BY
    datetime(utc_timestamp, 'unixepoch', 'localtime')
'''

html_parser = HTMLParser.HTMLParser()

stop = nltk.corpus.stopwords.words("english")
stop.append('rt')

contractions = []
with open('contractions.txt', 'rb') as f:
    contractions = [c.strip() for c in f.readlines()]

lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

url_regex = re.compile(r"http[s]?[^\s]*")
contractions_regex = re.compile("|".join(contractions))

first_tweet = None

con = sqlite3.connect("/home/maroy/idx.db")
c = con.cursor()

limit_idx = 0
limit = limits[0]
output_files = OutputFiles(limit)

sys.stdout.write('.')

for row in c.execute(query):
    created = row[0]

    if created >= limits[limit_idx+1]:
        output_files.close()
        limit_idx += 1
        limit = limits[limit_idx]
        output_files = OutputFiles(limit)
        sys.stdout.write('.')
        sys.stdout.flush()

    # print type(created), type(limits[0]), type(limits[1])
    # print created, limits[0], limits[1]
    # print created >= limits[0], created < limits[1]

    text = row[1]
    text = html_parser.unescape(text)
    text = text.lower()

    text = url_regex.sub('', text)
    text = contractions_regex.sub('', text)

    all_tokens = tokenizer.tokenize(text)
    tokens = []
    for token in all_tokens:
        token = lemmatizer.lemmatize(token)
        if token not in stop:
            tokens.append(token)

    items = [token.encode('utf8') for token in tokens]
    output_files.write(" ".join(items))

output_files.close()
con.close()

print 'done: ' + str(datetime.datetime.now())