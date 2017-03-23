from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import sys
sys.path.append("~/ex2Files")
from myDBObj import *


class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.db = PgDBConnection()

        if not self.db.bInit:
            # cannot proceed
            sys.exit("database complications")

        # since the use case here is live analysis,
        # drop the contents of the db table before each run
        try:
            cur = self.db.conn.cursor()
            cur.execute("DELETE * FROM tweetwordcount;")
            self.db.conn.commit()
            
        except Exception as e:
            # this seems to throw an exception when there are no rows to delete, which happens
            # every run for all but one of the word counters. So, no need to print the error,
            # just clean it up
            self.db.conn.rollback()
#            self.log('%s\n' % e)
        
        finally:
            cur.close()

    def process(self, tup):
        uWord = tup.values[0]

        # Increment the DB count
        try:
            cur = self.db.conn.cursor()
            cur.execute("UPDATE tweetwordcount SET count = count + 1 WHERE word=%s;", [uWord])
            self.db.conn.commit()
            
            if cur.rowcount == 0:
                cur.execute("INSERT INTO tweetwordcount (word,count) VALUES (%s, 1);", [uWord]);
                self.db.conn.commit()
                cur.close()
        
        except Exception as e:
            self.log('%s' % e)

        # Increment the local count
        self.counts[uWord] += 1
        self.emit([uWord, self.counts[uWord]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (uWord, self.counts[uWord]))
