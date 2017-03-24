##
## Running the ExTweetWordCount Application
##

To run the application, 
Edit the config.ini file and fill in Twitter Application credentials. 

Make sure Postgres is running. 

Run the runDemo.sh script to see the stream in action. 

The script has one optional parameter which is a comma separated list of words to track.
That is, only tweets containing words in this list will be tracked. 

Ex) ./RunDemo.sh track,Track,words,like,these

Note track words are case sensitive.
If this option is not supplied, the default value will be read from the config.ini file, 
As installed, the list contains “a,and,an,the,u,you”, however it can be edited manually if so desired.

Note that it is one parameter, and while spaces are not required, if they appear, “quotes” 
must be used on the command line. The application runs until terminated with “Ctrl+c”. 
Keep in mind that if left running, it will periodically stop because of Twitter’s rate limiting policy.