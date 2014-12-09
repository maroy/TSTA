import sys
import sqlite3
from dateutil import tz
import datetime

from_zone = tz.tzutc()
to_zone = tz.tzlocal()

con = sqlite3.connect(sys.argv[1])

counts = {}
for row in con.execute("SELECT utc_timestamp FROM tweets"):
    dt = datetime.datetime.utcfromtimestamp(row[0]).replace(tzinfo=from_zone).astimezone(to_zone)

    key = dt.strftime("%Y-%m-%d %H:%M")

    if key not in counts:
        counts[key] = 1
    else:
        counts[key] += 1

con.close()

with open("tpm.csv", "w") as f:
    for key in counts:
        f.write("{0},{1}\n".format(key, counts[key]))