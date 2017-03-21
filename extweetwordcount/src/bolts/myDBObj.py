#
# myDBObj.py
# open a db connection and maintain it for the duration of object life
# we aren't going to be very sophisticated here, and just create and manage
# the db and single table for w205 Exercise 2
# pass through standard operations
#
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class PgDBConnection:
    """Create the db and table, and connect. Simple wrapper to
    ensure the connection is closed on exit"""

    def __init__(self):
        
        self.bInit = False;
        self.defaultDB = "postgres"
        self.database = "tcount"
        self.user = "postgres"
        self.password = "pass"
        self.host = "localhost"
        self.port = "5432"
        
        # Connect to the database
        try:
            self.conn = psycopg2.connect( database = self.database,
                                          user = self.user,
                                          password = self.password,
                                          host = self.host,
                                          port = self.port)
            self.bInit = True
        except:
            # nothing fancy, just assume the db isn't created yet
            pass
        
        #Create the Database
        if not self.bInit:
            try:
                # CREATE DATABASE can't run inside a transaction
                self.conn = psycopg2.connect( database = self.defaultDB,
                                              user = self.user,
                                              password = self.password,
                                              host = self.host,
                                              port = self.port)
                self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                cur = self.conn.cursor()
                cur.execute("CREATE DATABASE " + self.database)
                self.bInit = True
                cur.close()
                self.conn.close()
                print "Created database tcount"

            except psycopg2.Error as e:
                print e.pgerror
                
            # db created, connection should work
            if self.bInit:
                try:
                    self.conn = psycopg2.connect( database = self.database,
                                                  user = self.user,
                                                  password = self.password,
                                                  host = self.host,
                                                  port = self.port)

                except psycopg2.Error as e:
                    self.bInit = False
                    print e.pgerror
                    
        # make sure the tweetwordcount table is created
        if self.bInit:
            try:
                # create tweetwordcount table
                cur = self.conn.cursor()
                cur.execute('''CREATE TABLE tweetwordcount
                       (word TEXT PRIMARY KEY     NOT NULL,
                       count INT     NOT NULL);''')
                self.conn.commit()
                print "Created table tweetwordcount"
            except psycopg2.Error as e:
                # it is only an error if it is not an already exists error
                if "already exists" not in e.pgerror:
                    self.bInit = False
                    print e.pgerror
                self.conn.rollback()
            finally:
                cur.close()
    
    # close the connection on exit
    def __del__(self):
        if self.bInit:
            self.conn.close()
            self.bInit = False


