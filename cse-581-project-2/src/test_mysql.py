import sqlite3
import mysql.connector

idx_db = sqlite3.connect('../data/idx.db')
idx_db_cur = idx_db.cursor()

tools_tb = mysql.connector.connect(host='192.168.56.101', db='project_two', user='tools', passwd='password')
tools_tb_cur = tools_tb.cursor()

idx_db_cur.execute('select db, id, created, utc_timestamp, screen_name, content from tweets')
for row in idx_db_cur:
    tools_tb_cur.execute(
        "INSERT INTO tweets(source_db, source_db_id, created, utc_timestamp, screen_name, tweet_text) VALUES (%s, %d, %s, %f, %s, %s)",
        (str(row[0]), row[1], str(row[2]), row[3], str(row[4]), str(row[5]))
    )
tools_tb.commit()


tools_tb_cur.close()
tools_tb.close()

idx_db_cur.close()
idx_db.close()
