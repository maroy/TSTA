import re
import sys
import sqlite3

from keyword_extractor import KeywordExtractor

def main():

    include_regex = re.compile(r'\bnfl\b', re.IGNORECASE)
    exclude_regex = re.compile(r'\bnba\b|\bnhl\b', re.IGNORECASE)

    extractor = KeywordExtractor()

    idx_db = sqlite3.connect('../idx.db')
    idx_db_cur = idx_db.cursor()

    nfl_db = sqlite3.connect('../nfl_tweets.db')
    nfl_db_cur = nfl_db.cursor()

    print "Getting already added ids"
    already_added_ids = set()
    nfl_db_cur.execute('SELECT idx_id FROM nfl_tweets')
    for row in nfl_db_cur:
        already_added_ids.add(row[0])

    print "Found {0} ids".format(len(already_added_ids))

    count = 0

    idx_db_cur.execute("SELECT rowid, utc_timestamp, content FROM tweets")
    for row in idx_db_cur:
        if row[0] not in already_added_ids:
            if include_regex.search(row[2]) is not None and exclude_regex.search(row[2]) is None:

                keywords = extractor.extract(row[2])

                if 'nfl' in keywords:
                    count += 1
                    nfl_db_cur.execute(
                        'INSERT INTO nfl_tweets(idx_id,created,keywords) VALUES(?,?,?)',
                        (row[0],row[1],keywords)
                    )

                    if count > 0 and count % 10000 == 0:
                        sys.stdout.write('.')
                        sys.stdout.flush()

    if count > 10000:
        print
        print 'added', count, 'records'
        print 'committing'
    else:
        print 'nothing new found'

    nfl_db.commit()
    print 'closing'

    nfl_db_cur.close()
    nfl_db.close()    

    idx_db_cur.close()
    idx_db.close()


if __name__ == "__main__":
    main()
