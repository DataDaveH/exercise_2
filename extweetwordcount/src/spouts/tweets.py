from __future__ import absolute_import, print_function, unicode_literals
import sys, os
import itertools, time
import tweepy, copy 
import Queue, threading
import ConfigParser

from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################

##{
##    "consumer_key"        :  "hSRTIgIOcRlducBVkUJJr8AIV",
##    "consumer_secret"     :  "bQohiy0n3gUrAUfXtDwxVTE5LZg7NcXzCFGTpyDWRIiyLnAoma",
##    "access_token"        :  "843594662606602240-j3qA2UWgPEtoWMQhfWuwHQMDpleRq01",
##    "access_token_secret" :  "lMJMGL7zXJEvrEigy92EwbzmJ3dwbi66acJ1UfPZ0F9FQ",
##}

# twitter_credentials are in section 'CREDENTIALS' in the config file
def auth_get(auth_key, config):
    try:
        if auth_key in config.options('CREDENTIALS'):
            return config.get('CREDENTIALS', auth_key)
    except:
        return None

################################################################################
# Class to listen and act on the incoming tweets
################################################################################
class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    def on_status(self, status):
        self.listener.queue().put(status.text, timeout = 0.01)
        return True
  
    def on_error(self, status_code):
        return True # keep stream alive
  
    def on_limit(self, track):
        return True # keep stream alive

class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 100)

        config = ConfigParser.ConfigParser()
        try:
            config.read(os.path.expanduser('~/ex2Files/config.ini'))
        except:
            sys.exit("Cannot read config file")

        try:
            trackString = config.get('OPTIONS', 'track')
            
            # strip out extra quotes and spaces
            track = [i.strip() for i in trackString.strip('"\'').split(',')]
        except Exception as e:
            track = ['a', 'an', 'and', 'the', 'you', 'u']
            self.log('\n\n\nUnable to read track option from config file, defaulting to: ' \
                 + ','.join(track) + '\n\n\n')
        
        try:
            consumer_key = auth_get("consumer_key", config)
            consumer_secret = auth_get("consumer_secret", config)
            print(consumer_key + '\n\t' + consumer_secret, file=sys.stderr)
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            
            if auth_get("access_token", config) and \
               auth_get("access_token_secret", config):
                access_token = auth_get("access_token", config)
                access_token_secret = auth_get("access_token_secret", config)
                auth.set_access_token(access_token, access_token_secret)
        except:
            sys.exit('Credentials problem, check config file')

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, listener, timeout=None)
        stream.filter(languages=["en"], track=track, async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1) 
            if tweet:
                self.queue().task_done()
                self.emit([tweet])
 
        except Queue.Empty:
#            self.log("Empty queue exception ")
            time.sleep(0.1) 

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        pass  # if a tuple fails to process, do nothing
