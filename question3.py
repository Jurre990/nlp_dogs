import nltk
from nltk import ngrams
import json
from collections import defaultdict
import pickle

def load_reddit_comment_data():

    submissions_data = []
    comments_data = []

    with open("dataset_folder/dogs_submissions.ndjson", 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            submissions_data.append(data)

    with open("dataset_folder/dogs_comments.ndjson", 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            comments_data.append(data)

    comments_data = [ i["body"].lower() for i in comments_data]
    submissions_data = [ i["selftext"].lower() for i in submissions_data]

    return submissions_data+comments_data

#nltk.download('punkt_tab')
load_data = False

if load_data:
    with open("model", "rb") as fp:   # Unpickling
        model = pickle.load(fp)
else:
    text = load_reddit_comment_data()


    print("Creating ngram")

    ngram = []
    for i in range(1000):
        print(i)
        ngram = ngram + (list(ngrams(text[i].split(" "), 4)))


    # Build a trigram model
    model = dict(dict())

    # Count frequency of co-occurrence
    #print(ngram)
    for w1, w2, w3, w4 in ngram:
        try:
            model[(w1, w2, w3)][w4] += 1
        except:
            model[(w1, w2, w3)] = {}
            model[(w1, w2, w3)][w4] = 1

    # Transform the counts into probabilities
    for w1_w2 in model:
        total_count = float(sum(model[w1_w2].values()))
        for w4 in model[w1_w2]:
            model[w1_w2][w4] /= total_count

    #model = dict(model)

    with open("model", "wb") as fp:   #Pickling
        pickle.dump(model, fp)

# Function to predict the next word
def predict_next_word(w1, w2, w3):
    """
    Predicts the next word based on the previous two words using the trained trigram model.
    Args:
    w1 (str): The first word.
    w2 (str): The second word.

    Returns:
    str: The predicted next word.
    """
    next_word = model[w1, w2, w3]
    if next_word:
        predicted_word = max(next_word, key=next_word.get)  # Choose the most likely next word
        return predicted_word
    else:
        return "No prediction available"


sentence = ['train', 'your', 'dog']
for i in range(100):
    next_word = predict_next_word(sentence[0], sentence[1], sentence[2])
    print(next_word)
    sentence = sentence[1:]
    sentence.append(next_word)
