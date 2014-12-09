import sys
import json
import sqlite3

db_name = sys.argv[1]
print db_name
con = sqlite3.connect(db_name)
c = con.cursor()

sql = "SELECT inserted, contents FROM stream_results ORDER BY inserted"

c.execute(sql)
count = 0
for row in c:
    tweet = json.loads(row[1])
    print tweet["lang"], tweet["user"]["screen_name"]
    try:
        print tweet["text"]
    except:
        print ":("
    count += 1
con.close()

print count

