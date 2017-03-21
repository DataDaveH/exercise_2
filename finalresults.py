#
# finalresults.py
#
import sys
import myDBObj

#set up db
db = PsDBConnection()
if not db.bInit:
    sys.exit()

# if we are investigating a particular word
if len( sys.argv > 1):
    searchWord = sys.argv[1]
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT count from tweetwordcount where word=%s", [searchWord])
        
        records = cur.fetchall()
        if len(records) == 0:
            print( "Total number of occurrences of '%s': 0" % (searchWord))
        else:
            for rec in records:
                print( "Total number of occurrences of '%s': %d" % (searchWord, rec[0]))
        db.conn.commit()

    except Exception as e:
        print( "Total number of occurrences of '%s': 0" % (searchWord))
        #print(e)
# print them all
else:
    try:
        cur = db.conn.cursor()
        cur.execute("SELECT word, count from tweetwordcount order by word")
        records = cur.fetchmany(1000)
        while records:
            for rec in records:
                print(rec)
            records = cur.fetchmany(1000)
        db.conn.commit()

    except Exception as e:
        print(e)





