# Pad naar de bestanden
file_paths = [
    "dataset_folder/dogs_submissions.ndjson",
    "dataset_folder/dogs_comments.ndjson"
]

# Lees en print de eerste 5 regels van elk bestand
for file_path in file_paths:
    print(f"Bestand: {file_path}")
    try:
        # Open het bestand en lees de eerste 2 regels
        with open(file_path, "r") as file:
            for i in range(2):  # Alleen de eerste 2 regels
                print(file.readline().strip())
        print("\n")  # Scheiding tussen bestanden
    except Exception as e:
        print(f"Kon bestand niet openen: {e}\n")


# Zorg dat NLTK weet waar het moet zoeken
nltk.data.path.clear()  # Leeg eventueel bestaande paden
nltk.data.path.append(nltk_data_path)

nltk.download('wordnet', download_dir=nltk_data_path, force=True)
nltk.download('omw-1.4', download_dir=nltk_data_path, force=True)

print(os.listdir(nltk_data_path))  # Zou 'corpora' moeten tonen
print(os.listdir(os.path.join(nltk_data_path, "corpora")))  # Zou 'wordnet' moeten tonen

import zipfile
import os

corpora_path = os.path.join(nltk_data_path, "corpora")

# Pak wordnet.zip uit in corpora/wordnet/
with zipfile.ZipFile(os.path.join(corpora_path, "wordnet.zip"), 'r') as zip_ref:
    zip_ref.extractall(os.path.join(corpora_path, "wordnet"))

# Pak omw-1.4.zip uit in corpora/omw-1.4/
with zipfile.ZipFile(os.path.join(corpora_path, "omw-1.4.zip"), 'r') as zip_ref:
    zip_ref.extractall(os.path.join(corpora_path, "omw-1.4"))

from nltk.corpus import wordnet
wordnet.ensure_loaded()

from nltk.corpus import wordnet

# Controleer of WordNet werkt door een synoniem op te halen
def test_wordnet():
    try:
        syns = wordnet.synsets("dog")
        print("Test geslaagd: WordNet is correct geladen.")
        print(f"Voorbeeld synoniemen voor 'dog': {[syn.name() for syn in syns[:5]]}")
    except Exception as e:
        print(f"Fout bij het testen van WordNet: {e}")

# Voer de test uit
test_wordnet()
#!pip install --upgrade nltk

import json
import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
nltk.download('punkt_tab')

# Mapping van resources naar hun NLTK-data paden
RESOURCE_PATHS = {
    'punkt': 'tokenizers/punkt',
    'stopwords': 'corpora/stopwords',
    'wordnet': 'corpora/wordnet'
}

def ensure_nltk_resources():
    nltk_data_path = "/usr/share/nltk_data"  # Alternatieve locatie
    if not os.path.exists(nltk_data_path):
        os.makedirs(nltk_data_path)
    nltk.data.path.append(nltk_data_path)
    
    for resource in ['punkt', 'stopwords', 'wordnet']:
        resource_path = RESOURCE_PATHS[resource]
        try:
            nltk.data.find(resource_path)
        except LookupError:
            print(f"Downloading missing resource: {resource}")
            nltk.download(resource, download_dir=nltk_data_path, quiet=False, force=True)
            # Na het downloaden nogmaals controleren
            nltk.data.find(resource_path)

# Zorg ervoor dat alle NLTK-resources beschikbaar zijn
ensure_nltk_resources()

english_stopwords = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text, remove_empty=True):
    if text.strip().lower() in ['[removed]', '[deleted]']:
        return None
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in english_stopwords]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    if remove_empty and len(tokens) == 0:
        return None
    return tokens

# Lees lijst met hondenrassen in
dog_breeds_file = "Dog_Breeds_List.txt"
with open(dog_breeds_file, "r", encoding="utf-8") as f:
    dog_breeds_raw = f.readlines()
dog_breeds = [breed.strip().lower() for breed in dog_breeds_raw if breed.strip()]

submissions_file = "dataset_folder/dogs_submissions.ndjson"
comments_file = "dataset_folder/dogs_comments.ndjson"

cleaned_submissions = []
cleaned_comments = []

# Preprocess submissions
with open(submissions_file, 'r', encoding='utf-8') as f:
    for line in f:
        submission_data = json.loads(line)
        raw_text = submission_data.get('selftext', '')
        cleaned = clean_text(raw_text)
        if cleaned is not None:
            submission_data['tokens'] = cleaned
            cleaned_submissions.append(submission_data)

# Preprocess comments
with open(comments_file, 'r', encoding='utf-8') as f:
    for line in f:
        comment_data = json.loads(line)
        raw_text = comment_data.get('body', '')
        cleaned = clean_text(raw_text)
        if cleaned is not None:
            comment_data['tokens'] = cleaned
            cleaned_comments.append(comment_data)

if cleaned_submissions:
    print("Voorbeeld tokens van eerste submission:", cleaned_submissions[0]['tokens'][:5])

if cleaned_comments:
    print("Voorbeeld tokens van eerste comment:", cleaned_comments[0]['tokens'][:5])


from collections import Counter

breed_counter = Counter()

# Tel in submissions
for sub in cleaned_submissions:
    tokens = sub['tokens']
    for token in tokens:
        if token in dog_breeds:
            breed_counter[token] += 1

# Tel in comments
for com in cleaned_comments:
    tokens = com['tokens']
    for token in tokens:
        if token in dog_breeds:
            breed_counter[token] += 1

# Print de top 10 meest voorkomende rassen
print(breed_counter.most_common(10))

length = len(breed_tokens)
# Loop over tokens met een sliding window van de breed-lengte
for i in range(len(tokens)-length+1):
    # Vergelijk slice van tokens met de rasnaam-lijst
    if tokens[i:i+length] == breed_tokens:
        # Verhoog de teller met de originele rasnaam (voeg ze weer samen)
        breed_name = " ".join(breed_tokens)
        breed_counter[breed_name] += 1

for com in cleaned_comments:
    tokens = com['tokens']
    for breed_tokens in dog_breeds_tokenized:
        length = len(breed_tokens)
        for i in range(len(tokens)-length+1):
            if tokens[i:i+length] == breed_tokens:
                breed_name = " ".join(breed_tokens)
                breed_counter[breed_name] += 1

# Print de top 10 meest voorkomende rassen (inclusief meerwoordige)
print(breed_counter.most_common(10))
