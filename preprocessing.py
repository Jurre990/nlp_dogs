import json

def load_reddit_comment_data(data_directory):

    comments_data = [] # list object that will store the loaded Reddit comments

    # we first open the file that includes our dataset
    with open(data_directory, 'r', encoding='utf-8') as f:
        # iterate the file, reading it line by line
        for line in f:
            # load the data petraining to a line into a json object in memory
            data = json.loads(line)

            # append the comment
            comments_data.append(data)

    # the method returns all the loaded Reddit comments
    return comments_data

# our data is stored in this file
file_paths = [
    "dataset_folder/dogs_submissions.ndjson",
    "dataset_folder/dogs_comments.ndjson"
]
# lets load our dataset into memory
reddit_data = load_reddit_comment_data(file_paths[0])
print(reddit_data[0]["selftext"].lower())