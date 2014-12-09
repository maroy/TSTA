import re
import sys
import sqlite3

from keyword_extractor import KeywordExtractor

def main():
    extractor = KeywordExtractor()

    idx_db = sqlite3.connect('../idx.db')
    idx_db_cur = idx_db.cursor()

    kwd_db = sqlite3.connect('../kwd.db')
    kwd_db_cur = kwd_db.cursor()

    print "Getting already added ids"
    already_added_ids = set()
    kwd_db_cur.execute('SELECT idx_id FROM keywords')
    for row in kwd_db_cur:
        already_added_ids.add(row[0])

    print "Getting found {0} ids".format(len(already_added_ids))

    count = 0

    idx_db_cur.execute("SELECT rowid, utc_timestamp, content FROM tweets")
    for row in idx_db_cur:
        if row[0] not in already_added_ids:
            count += 1
            keywords = extractor.extract(row[2])

            kwd_db_cur.execute(
                'INSERT INTO keywords(idx_id,created,content) VALUES(?,?,?)',
                (row[0],row[1],keywords)
            )

            if count > 0 and count % 10000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()

    if count > 10000:
        print
        print 'committing'
    else:
        print 'nothing new found'

    kwd_db.commit()
    print 'closing'

    kwd_db_cur.close()
    kwd_db.close()    

    idx_db_cur.close()
    idx_db.close()


if __name__ == "__main__":
    main()
