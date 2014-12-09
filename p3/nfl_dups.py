import sqlite3

db = sqlite3.connect('../nfl_tweets.db')

dups = {}

for row in db.execute("SELECT keywords FROM nfl_tweets"):
	kw = row[0]

	if kw in dups:
		dups[kw] += 1
	else:
		dups[kw] = 1

db.close()

for kw in dups:
	if dups[kw] > 1:
		print kw, dups[kw]