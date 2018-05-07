#import python libaries used
from textblob import TextBlob
import sys, tweepy, csv, re
import matplotlib.pyplot as plt


def percentage(part, whole):
    return 100 * float(part)/float(whole)

#authenticate with Twitter API
consumerKey = ""
consumerSecret = ""
accessToken = ""
accessTokenSecret = ""

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

#query
searchTerm = "#scotrail"
noOfTerms = 100

tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfTerms)

#write text file
with open('Tweet_Sentiments.csv', 'w') as pointer:
    newFileWriter = csv.writer(pointer)
    newFileWriter.writerow(['Tweet', 'Sentiment'])


positive = 0
negative = 0    
neutral = 0



for tweet in tweets:
    analysis = TextBlob(tweet.text) #analysis sentiment polarity
    print(tweet.text)
    print(tweet.created_at)
    print(analysis.sentiment.polarity)
    print("---")
   
    #write text file
    with open('Tweet_Sentiments.csv', 'a') as pointer:
        newFileWriter = csv.writer(pointer)
        newFileWriter.writerow([tweet.text.encode('utf-8')])
        newFileWriter.writerow([analysis.sentiment.polarity])

    #register as positive/negative/neutral for % purposes
    if (analysis.sentiment.polarity > 0.00):
        positive += 1
    elif (analysis.sentiment.polarity < 0.00):
        negative += 1
    elif (analysis.sentiment.polarity == 0.00): 
        neutral += 1




positive = percentage(positive, noOfTerms)
negative = percentage(negative, noOfTerms)
neutral = percentage(neutral, noOfTerms)


#pie graph
labels = ['Positive [' + str(positive) + '%]', 'Negative [' + str(negative) + '%]', 'Neutral [' + str(neutral) + '%]']
sizes = [positive, negative, neutral]
colors = ['yellowgreen', 'red', 'gold']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title('How people are reacting to ' + searchTerm + ' by analyzing ' + str(noOfTerms) + ' Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()

            

