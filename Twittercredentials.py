import tweepy

consumer_key = "hSRTIgIOcRlducBVkUJJr8AIV";
#eg: consumer_key = "YisfFjiodKtojtUvW4MSEcPm";


consumer_secret = "bQohiy0n3gUrAUfXtDwxVTE5LZg7NcXzCFGTpyDWRIiyLnAoma";
#eg: consumer_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token = "843594662606602240-j3qA2UWgPEtoWMQhfWuwHQMDpleRq01";
#eg: access_token = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";

access_token_secret = "lMJMGL7zXJEvrEigy92EwbzmJ3dwbi66acJ1UfPZ0F9FQ";
#eg: access_token_secret = "YisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPmYisfFjiodKtojtUvW4MSEcPm";


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



