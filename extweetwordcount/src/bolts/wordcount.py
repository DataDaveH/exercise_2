from __future__ import absolute_import, print_function, unicode_literals

from collections import Counter
from streamparse.bolt import Bolt
import myDBObj
import sys

class WordCounter(Bolt):

    def initialize(self, conf, ctx):
        self.counts = Counter()
        self.db = myDBObj.PgDBConnection()

        if !self.db.bInit:
            # cannot proceed
            sys.exit("database complications")

        # since the use case here is live analysis,
        # drop the contents of the db table before each run
        cur = self.db.conn.cursor()
        cur.execute("DELETE FROM tweetwordcount)
        self.db.conn.commit()
        cur.close()
    
    def process(self, tup):
        uWord = tup.values[0]

        # Increment the DB count
        cur = self.db.conn.cursor()
        cur.execute("UPDATE tweetwordcount SET count = count + 1 WHERE word=%s", uWord)
        self.db.conn.commit()
        if cur.rowcount == 0:
            # first time for this word, so insert instead
            cur.execute("INSERT INTO tweetwordcount (word,count) VALUES ('%s', 1)", uWord);
            self.db.conn.commit()
        cur.close()

        # Increment the local count
        self.counts[word] += 1
        self.emit([word, self.counts[word]])

        # Log the count - just to see the topology running
        self.log('%s: %d' % (word, self.counts[word]))
