import re
import sys
import json
import sqlite3
import datetime
import dateutil
from keyword_collector import KeywordCollector
#from tweet_collector import TweetCollector
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def cluster(data, k):

    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

    with open('data.txt', 'wb') as f:
        f.write("\n".join(data).encode('utf8'))

    td_matrix = vectorizer.fit_transform(data)
    km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1, n_jobs=-1)
    km.fit(td_matrix)
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    result = []

    for i in range(k):
        result.append([])
        for ind in order_centroids[i, :10]:
            result[i].append(terms[ind])

    return result


def dot():
    sys.stdout.write('.')
    sys.stdout.flush()

'''
with open('contractions.txt', 'rb') as f:
    contractions = [c.strip().lower() for c in f.readlines()]
contractions_regex = re.compile("|".join(contractions), re.IGNORECASE)


clean_regex = re.compile(r"http[s]?[^\s]*|\brt\b", re.IGNORECASE)

def clean_tweet(tweet, other_re=None):
    tweet = clean_regex.sub('', tweet)
    tweet = contractions_regex.sub('', tweet)

    if other_re is not None:
        tweet = other_re.sub('', tweet)

    return tweet
'''

def main():

    label = sys.argv[1]
    duration = int(sys.argv[2])

    regexes = {
        'nba': re.compile(r'\bnba\b'),
        'nfl': re.compile(r'\bnfl\b'),
        'nhl': re.compile(r'\bnhl\b'),
        'any': re.compile(r'\bnba\b|\bnfl\b|\bnhl\b')
    }

    regex = regexes[label]


    db = sqlite3.connect('../kwd.db')
    collector = KeywordCollector(db)

    #db = sqlite3.connect('../idx.db')
    #collector = TweetCollector(db)

    results = []

    for day in range(6,13):
        for hour in range(0,24):
            for minute in [0,30]:
                end = datetime.datetime(2014,11,day,hour, minute, tzinfo=dateutil.tz.tzlocal())
                start = end - datetime.timedelta(seconds=60 * duration)

                data = collector.collect(start,end)

                result_date = end.strftime('%Y-%m-%d %H:%M')
                result_clusters = []

                if label == 'any':
                    cleaned = [d for d in data]
                else:
                    cleaned = [regex.sub('', d) for d in data if regex.search(d) is not None]

                if len(cleaned) > 1:
                    result_clusters = cluster(cleaned,3)
                
                results.append({"date": result_date, "clusters": result_clusters})

                dot()
    print
    db.close()

    with open('viz/' + label + ".json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()
