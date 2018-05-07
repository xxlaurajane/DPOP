import tweepy
import csv
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

def percentage(part, whole):
    return 100 * float(part)/float(whole)


consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)



csvFile = open('lols.csv', 'w')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["Time", "Tweet", "Sentiment"])

searchTerm = "#scotrail"
noOfTerms = 100

tweets = tweepy.Cursor(api.search,q=searchTerm).items(noOfTerms*3)
#tweets = tweepy.Cursor(api.search,q=searchTerm, since="2018-03-09").items(noOfTerms*3)

positive = 0
negative = 0    
neutral = 0

count = 1
for tweet in tweets:
    tweetText = re.sub('[^A-Za-z0-9 ]+', '', tweet.text)
    if (count <= noOfTerms):
        if not (tweetText.startswith("RT")):
            analysis = TextBlob(tweet.text)                     
            if (analysis.sentiment.polarity > 0.00):
                positive += 1
                count = count + 1
            elif (analysis.sentiment.polarity < 0.00):
                negative += 1
                count = count + 1
            elif (analysis.sentiment.polarity == 0.00): 
                neutral += 1
                count = count + 1

            print (tweet.created_at, tweetText, analysis.sentiment.polarity)
            csvWriter.writerow([tweet.created_at, tweetText, analysis.sentiment.polarity])

count = count - 1
print ("Tweet count: " + str(count))
csvFile.close()

positive = percentage(positive, count)
negative = percentage(negative, count)
neutral = percentage(neutral, count)



labels = ['Positive [' + str(positive) + '%]', 'Negative [' + str(negative) + '%]', 'Neutral [' + str(neutral) + '%]']
sizes = [positive, negative, neutral]
colors = ['yellowgreen', 'red', 'gold']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('How people are reacting to ' + searchTerm + ' by analyzing ' + str(count) + ' Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()