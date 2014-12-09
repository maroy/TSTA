import sqlite3

sql = '''
SELECT
	strftime('%d',datetime(utc_timestamp, 'unixepoch', 'localtime')),
	content
from
	tweets;
'''

def write_tweets(day, tweets):
	with open('/Users/maroy/TWEET_TEXT/{0}.txt'.format(day), 'w') as f:
		f.writelines([line + "\n" for line in tweets])

def main():
	last_day = "00"
	tweets = None
	con = sqlite3.connect('/Users/maroy/TWEETS/idx.db')

	for row in con.execute(sql):
		day = row[0]
		tweet = row[1].encode('utf-8').encode('string-escape')

		if last_day == "00":
			last_day = day
			tweets = [tweet]
		elif day != last_day:
			write_tweets(last_day, tweets)
			last_day = day
			tweets = [tweet]
		else:
			tweets.append(tweet)

	con.close()


if __name__ == '__main__':
	main()
