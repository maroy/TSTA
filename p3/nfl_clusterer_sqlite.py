import re
import sys
import json
import sqlite3
import datetime
import dateutil
import numpy
from keyword_collector import KeywordCollector
#from tweet_collector import TweetCollector
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

sql = '''
SELECT
    keywords
FROM
    nfl_tweets
WHERE
    created >= ?
    AND
    created < ?
'''

utc_epoch = datetime.datetime(1970,1,1,tzinfo=dateutil.tz.tzutc())

def to_utc_timestamp(dt):
    return (dt - utc_epoch).total_seconds()

def collect_tweets(db, start, end):
    start = to_utc_timestamp(start)
    end = to_utc_timestamp(end)

    data = [row[0] for row in db.execute(sql, (start, end))]

    return data


def cluster(data, k):

    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=['nfl','game','team'])

    td_matrix = vectorizer.fit_transform(data)
    km = KMeans(n_clusters=k, init='k-means++', max_iter=300, n_jobs=-1)
    km.fit(td_matrix)
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    def count(acc,value):
        acc[value] += 1
        return acc

    cluster_counts = reduce(count, km.labels_, [0]*k)

    #_max = (0,0)
    #for i in range(0,len(cluster_counts)):
    #    if _max[1] < cluster_counts[i]:
    #        _max = (i,cluster_counts[i])

    #print _max[0], _max[1], float(_max[1]) / len(data)
    # print counts

    result = []

    for i in reversed(numpy.array(cluster_counts).argsort()):
        x = [float(cluster_counts[i])/len(data)]
        for ind in order_centroids[i, :10]:
            x.append(terms[ind])
        result.append(x)

    return result


def dot():
    sys.stdout.write('.')
    sys.stdout.flush()

def main():

    duration = 240

    db = sqlite3.connect('../nfl_tweets.db')

    results = []

    for day in range(6,13):
        for hour in range(0,24):
            for minute in [0,15,30,45]:
                end = datetime.datetime(2014, 11, day, hour, minute, tzinfo=dateutil.tz.tzlocal())
                start = end - datetime.timedelta(seconds=60 * duration)

                data = collect_tweets(db,start,end)

                if len(data) == 0:
                    break

                result_date = start.strftime('%Y-%m-%d %H:%M') + " - " + end.strftime('%Y-%m-%d %H:%M')
                result_clusters = cluster(data,7)
                
                results.append({"date": result_date, "clusters": result_clusters})

                dot()
    print
    db.close()

    with open("viz/nfl.json", "w") as f:
        json.dump(results, f)

if __name__ == "__main__":
    main()
