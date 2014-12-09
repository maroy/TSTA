import re
import json
import sqlite3
import nltk

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

con = sqlite3.connect("D:/TWEETS/2014-11-05-22-45-54.db")
c = con.cursor()

with open("out.csv", "wb") as out_file:
    for row in c.execute("SELECT tweet FROM tweets"):
        if first_tweet is None:
            first_tweet = row[0]
        j = json.loads(row[0])
        tweet_id = j['id']
        timestamp = j['timestamp_ms']

        text = j['text']
        text = text.lower()

        text = url_regex.sub('', text)
        text = contractions_regex.sub('', text)

        all_tokens = tokenizer.tokenize(text)
        tokens = []
        for token in all_tokens:
            token = lemmatizer.lemmatize(token)
            if token not in stop:
                tokens.append(token)

        #items = [str(id), json.dumps(text)] + [token.encode('utf8') for token in tokens]
        items = [str(tweet_id), str(timestamp)] + [token.encode('utf8') for token in tokens]
        out_file.write(" ".join(items) + "\n")

with open("tweet.json", "wb") as f:
    f.write(first_tweet)

con.close()