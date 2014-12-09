import os
import re
import time
import datetime


class Tweets:

    def __init__(self):
        self.map = {}

    def process_folder(self, file_path):

        with open(file_path, 'rb') as f:
            for line in f:
                self.process_line(line)

    def process_line(self, line):
        parts = line.split(':', 1)

        dt = datetime.datetime.fromtimestamp(float(parts[0]))
        keywords = parts[1].strip()

        key = self.key_for_datetime(dt)

        if key in self.map:
            self.map[key].append(keywords)
        else:
            self.map[key] = [keywords]

    def key_for_datetime(self, dt):
        new_minute = 15 * (dt.minute / 15)
        return dt.replace(minute=new_minute).strftime('%m-%d-%H-%M')

    def get_collection(self, start, end, filter = None):
        collection = []

        if filter is not None:
            rex = re.compile(r'\b{0}\b'.format(filter))

        start_key = self.key_for_datetime(start)
        end_key = self.key_for_datetime(end)

        for key in sorted(self.map.keys()):
            if key >= start_key and key < end_key:
                for item in self.map[key]:
                    if filter is None or rex.search(item) is not None:
                        collection.append(item)

        return collection

    @staticmethod
    def load_from_folder(folder):
        tweets = Tweets()

        for fname in sorted(os.listdir(folder)):
            print "processing", fname
            tweets.process_folder(os.path.join(folder,fname))

        return tweets


if __name__ == "__main__":

    folder = '/Users/maroy/P2/text/'

    tweets = Tweets.load_from_folder(folder)

    collection = tweets.get_collection(datetime.datetime(2014,11,7), datetime.datetime(2014,11,14))
    print len(collection)

    collection = tweets.get_collection(datetime.datetime(2014,11,7), datetime.datetime(2014,11,14), 'nhl')
    print len(collection)

    collection = tweets.get_collection(datetime.datetime(2014,11,7), datetime.datetime(2014,11,14), 'nba')
    print len(collection)

    collection = tweets.get_collection(datetime.datetime(2014,11,7), datetime.datetime(2014,11,14), 'nfl')
    print len(collection)
