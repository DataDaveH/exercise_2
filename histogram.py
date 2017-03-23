#
# histogram.py
#
from __future__ import absolute_import
import sys
sys.path.append("~/ex2Files")
import myDBObj

#set up db
db = myDBObj.PgDBConnection()
if not db.bInit:
    sys.exit()

if (len(sys.argv) == 2) & (',' in sys.argv[1]):
    #see if we have lower,upper
    lower, upper = sys.argv[1].split(',')
elif len(sys.argv) == 3:
    lower = sys.argv[1]
    upper = sys.argv[2]
else:    
    print(sys.argv)
    print( """usage:\thistogram.py lower upper
          \nlower:\tlower bound\
          \nupper:\tupper bound
          \nreturns all the words with a total number of occurrences greater than or equal to\
          \nlower, and less than or equal to upper\n""")
    sys.exit()

try:
    cur = db.conn.cursor()
    cur.execute("SELECT word, count FROM tweetwordcount WHERE count >= %s AND count <= %s \
                 ORDER BY count DESC;", (lower, upper))
    records = cur.fetchmany(1000)
    while records:
        for rec in records:
            print("%s:\t%s" % (rec[0], rec[1]))
        records = cur.fetchmany(1000)
    db.conn.commit()

except Exception as e:
    print(e)









