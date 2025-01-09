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

#!pip install vaderSentiment
#from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Een functie om een sentimentscore te krijgen per document (sub/comm)
def get_sentiment(tokens):
    # Zet tokens om naar een string
    text = " ".join(tokens)
    return analyzer.polarity_scores(text)  # returns dict met {neg, neu, pos, compound}
breed_sentiments = {breed: [] for breed in dog_breeds}

for sub in cleaned_submissions:
    tokens = sub['tokens']
    sentiment = get_sentiment(tokens)
    # Check welke rassen hierin voorkomen
    mentioned_breeds = [t for t in tokens if t in dog_breeds]
    for mb in mentioned_breeds:
        breed_sentiments[mb].append(sentiment['compound'])

for com in cleaned_comments:
    tokens = com['tokens']
    sentiment = get_sentiment(tokens)
    mentioned_breeds = [t for t in tokens if t in dog_breeds]
    for mb in mentioned_breeds:
        breed_sentiments[mb].append(sentiment['compound'])
for breed, scores in breed_sentiments.items():
    if scores:
        avg_sent = sum(scores) / len(scores)
        print(breed, avg_sent)
