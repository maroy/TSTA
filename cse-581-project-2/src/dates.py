import sqlite3

con = sqlite3.connect('/Users/maroy/TWEETS/idx.db')
c = con.cursor()

last = None
for row in c.execute('SELECT utc_timestamp FROM tweets ORDER BY utc_timestamp'):
    current = row[0]
    if last is not None and current - last > 15:
      print last, ' -> ', current, current - last
    last = current
con.close()
