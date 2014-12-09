import re
import sys
import json
import time
import datetime
import numpy

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

from tweets import Tweets

tweets = None

def cluster(data, k, stop_words):

    vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words=stop_words)

    td_matrix = vectorizer.fit_transform(data)
    km = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_jobs=-1)
    km.fit(td_matrix)
    order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()

    def count(acc,value):
        acc[value] += 1
        return acc

    cluster_counts = reduce(count, km.labels_, [0]*k)

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

    t0 = time.time()

    folder = 'text/'

    tweets = Tweets.load_from_folder(folder)

    print "Tweets loaded {0}s".format(time.time() - t0)

    duration = 60
    results = []
    
    runs = [
        "nhl", "any", "nba", "nfl"
    ]
    
    for run in runs:
        t0 = time.time()
        for day in range(7,28):
            for hour in range(0,24):
                for minute in [0,15,30,45]:
                    end = datetime.datetime(2014, 11, day, hour=hour, minute=minute)
                    start = end - datetime.timedelta(seconds=60 * duration)

                    data = tweets.get_collection(start, end, run if run != 'any' else None)

                    if len(data) == 0:
                        break

                    result_date = start.strftime('%Y-%m-%d %H:%M') + " - " + end.strftime('%Y-%m-%d %H:%M')
                    result_clusters = cluster(data,5, [])
                    
                    results.append({"date": result_date, "clusters": result_clusters})

                    #dot()
                    print end, len(data)
        print

        with open("viz/" + run + "_15_60.json", "w") as f:
            json.dump(results, f)

        print run + ' done, ', time.time() - t0, 'seconds'

if __name__ == "__main__":
    main()
