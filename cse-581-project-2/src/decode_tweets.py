with open('/Users/maroy/TWEET_TEXT/05.txt') as f:
	lines = f.readlines()

print lines[0].decode('string-escape').decode('utf-8')