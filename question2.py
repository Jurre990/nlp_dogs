from pandas.io.sas.sas_constants import dataset_length
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

data = ['dogs are annoying', 'i love dogs'] # should be a list or array something that can be looped through
#the underlying funciton shows the average for the inputted data, we can solve question 2 by inputting the data per dog and getting the average

def average_sentiment(data)-> float:
    total = 0
    for text in data:
        scores = analyzer.polarity_scores(text)
        total += scores['compound']
    return total

print(average_sentiment(data))

