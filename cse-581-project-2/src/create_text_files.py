import json
import sqlite3
import nltk.corpus
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

con = sqlite3.connect("D:/TWEETS/2014-11-05-22-45-54.db")
c = con.cursor()

stop = nltk.corpus.stopwords.words("english")
stop.append('rt')
lemmatizer = WordNetLemmatizer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

first_tweet = None

s = set(1,2,3)
t = set(2,3,4)
s.intersection(t)

with open("out.csv", "wb") as out_file:
    for row in c.execute("SELECT tweet FROM tweets"):
        if first_tweet is None:
            first_tweet = row[0]
        j = json.loads(row[0])
        id = j['id']
        text = j['text'].lower()
        all_tokens = tokenizer.tokenize(text)
        tokens = set()
        for token in all_tokens:
            token = lemmatizer.lemmatize(token)
            if token not in stop:
                tokens.add(token)

        items = [str(id), json.dumps(text)] + [token.encode('utf8') for token in tokens]
        out_file.write(",".join(items) + "\n")

with open("tweet.json", "wb") as f:
    f.write(first_tweet)

con.close()