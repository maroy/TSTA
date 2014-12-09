import sqlite3
import dateutil.tz
from datetime import datetime

# created, datetime(created, 'unixepoch', 'localtime'), content

sql = '''
SELECT
    content
FROM
    tweets
WHERE
    utc_timestamp >= ?
    AND
    utc_timestamp < ?
'''

utc_epoch = datetime(1970,1,1,tzinfo=dateutil.tz.tzutc())

def to_utc_timestamp(dt):
    return (dt - utc_epoch).total_seconds()

class TweetCollector:

    def __init__(self, db):
        self.db = db

    def collect(self, start, end):
        text = ''

        start = to_utc_timestamp(start)
        end = to_utc_timestamp(end)

        data = [row[0] for row in self.db.execute(sql, (start, end))]

        return data


if __name__ == "__main__":
    db = sqlite3.connect('../idx.db')

    kc = TweetCollector(db)

    for d in range(5, 30):
        text = kc.collect(datetime(2014,11,d, tzinfo=dateutil.tz.tzlocal()), datetime(2014,11,d+1, tzinfo=dateutil.tz.tzlocal()))
        print len(text)

    db.close()