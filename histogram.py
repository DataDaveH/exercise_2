#
# histogram.py
#
import sys
import myDBObj

#set up db
db = PsDBConnection()
if not db.bInit:
    return None

if len(sys.argv) != 3:
   print( """usage:\thistogram.py lower, upper
          \nlower:\tlower bound\
          \nupper:\tupper bound
          \nreturns all the words with a total number of occurrences greater than or equal to\
          \nlower, and less than or equal to upper""")
   sys.exit()

lower = sys.argv[2]
upper = sys.argv[3]

try:
    cur = db.conn.cursor()
    cur.execute("SELECT word, count FROM tweetwordcount WHERE count >= %s AND count <= %s \
                 ORDER BY count DESC", (lower, upper))
    records = cur.fetchmany(1000)
    while records:
        for rec in records:
            print("%s:\t%s" % (rec[0], rec[1]))
        records = cur.fetchmany(1000)
    db.conn.commit()

except Exception as e:
    print(e)









