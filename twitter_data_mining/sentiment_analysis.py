"""
Ian Ashby
Twitter Data Mining Project

Get username from input, retrieve recent tweets, and perform a sentiment analysis on them.
"""
# Import packages
import pandas as pd
import tweepy
import requests
from textblob import TextBlob

# Connect to Twitter API and create client.
# Replace each token/key with your own by creating a Twitter dev account.
BEARER_TOKEN = ""
API_KEY = ""
API_SECRET_KEY = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

client = tweepy.Client( bearer_token=BEARER_TOKEN,
                        consumer_key=API_KEY,
                        consumer_secret=API_SECRET_KEY, 
                        access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_TOKEN_SECRET,
                        return_type=requests.Response,
                        wait_on_rate_limit=True)

# Prompt the user for a username and query data from the user input.
username = input("\nWho's tweets would you like to analyze? ")

# Use the username from input and filter out retweets, so we get original content from their timeline.
query = f'from:{username} -is:retweet'
tweets_query = client.search_recent_tweets(query=query, max_results=100)

# Save the data/query as dictionary. Extract the data.
tweets_dict = tweets_query.json() 
tweets_data = tweets_dict['data'] 

# Convert dictionary to a Pandas DF. 
df = pd.json_normalize(tweets_data)

# Loop through each tweet and analyze its corresponding sentiment. 
# Save sentiment into a list that will be added to the DF later.
sentiment_value = []
for tweet in df['text']:
      analysis = TextBlob(tweet)

      # set sentiment
      if analysis.sentiment.polarity > 0:
            sentiment_value.append('positive')
      elif analysis.sentiment.polarity == 0:
            sentiment_value.append('neutral')
      else:
            sentiment_value.append('negative')

# Add sentiment values to the DF.
df['sentiment'] = sentiment_value

# Isolate the positive and negative sentiments.
positive_tweets = df[df['sentiment'] =='positive']
negative_tweets = df[df['sentiment'] == 'negative']

# Calculate the percentage of each sentiment.
positive_percentage = (len(positive_tweets) / len(df) * 100)
negative_percentage = (len(negative_tweets) / len(df) * 100)

# Print the results.
print(f"\nHere is the sentiment analysis for @{username}: ")

print(f"Positive Tweet Percentage: {positive_percentage:.0f}%")
print(f"Negative Tweet Percentage: {negative_percentage:.0f}%")

print("\nPositive Tweet Samples:")
print(positive_tweets['text'][:5])

print("\nNegative Tweet Samples:")
print(negative_tweets['text'][:5])

