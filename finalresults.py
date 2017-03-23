#
# finalresults.py
#
#from __future__ import absolute_import
import sys
#sys.path.append("~/ex2Files")
import myDBObj

#set up db
db = myDBObj.PgDBConnection()
if not db.bInit:
    sys.exit()

# if we are investigating a particular word
if len( sys.argv) > 1:
    searchWord = sys.argv[1]
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT count from tweetwordcount where word=%s;", [searchWord])
        
        records = cur.fetchall()
        if len(records) == 0:
            print( "\nTotal number of occurrences of '%s': 0\n" % (searchWord))
        else:
            for rec in records:
                print( "\nTotal number of occurrences of '%s': %d\n" % (searchWord, rec[0]))
        db.conn.commit()

    except Exception as e:
        print(e)

# print them all
else:
    try:
        print(db.conn)
        cur = db.conn.cursor()
        cur.execute("SELECT word, count FROM tweetwordcount ORDER BY word;")
        records = cur.fetchmany(1000)
        while records:
            for rec in records:
                print(rec)
            records = cur.fetchmany(1000)
        db.conn.commit()

    except Exception as e:
        print(e)





