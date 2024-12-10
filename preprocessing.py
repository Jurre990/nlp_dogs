import json

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

reddit_data = load_reddit_comment_data()
print(reddit_data[0])
