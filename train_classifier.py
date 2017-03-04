# Read input data from mongo
# create feature vectors using 'bag of words' technique
# train Multinomial Naive Bayes algorithm
# Calculate the accuracy using K-fold technique

import sys
import numpy
from pymongo import MongoClient
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

# The pipeline classifier
# First, convert the input text data to feature vectors using CountVectorizer
# Then, feed this feature vector to Multinomial Naive Bayes Classifier
pipeline = Pipeline([
    ('vectorizer',  CountVectorizer(ngram_range=(1, 5))),
    ('tfidf_transformer',  TfidfTransformer()),
    #('classifier',  BernoulliNB(binarize=0.0)),
    #('classifier',  MultinomialNB()),
    ('classifier', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=19, random_state=42)),
    ])

# Number of folds to use in K-Folds Technique
NO_OF_FOLDS = 6

def initializeMongo(db_name, collection_name):
	client = MongoClient()
	db = client[db_name]
	collection = db[collection_name]
	return collection

# Read and return documents from collection_name in db_name of mongodb
# Filtered by group_name
def read_db_data(group_name, db_name, collection_name):

	collection = initializeMongo(db_name, collection_name)
	raw_data = collection.find({ 'group' : group_name})

	return raw_data

# Create a pandas data frame from raw documents data
def build_data_frame(raw_data):
	rows = []
	index = []

	for row in raw_data:
		rows.append({ 'text': row['text'], 'user': row['user'] })
		index.append(row['user'])

	data_frame = DataFrame(rows, index=index)
	print "Number of records: ", len(data_frame), "\n"

	print "Unique users: ", data_frame.user.unique()

	return data_frame

# Train the pipeline classifier with dataframe
def train_classifier(data):

	pipeline.fit(data['text'].values, data['user'].values)

#Once the classifier is trained, run some sample predictions on it
def run_predictions(input_texts):
	
	predictions = pipeline.predict(input_texts)
	
	for i in range(len(input_texts)):
		print "Message: ", input_texts[i], "\nPrediction: ", predictions[i], "\n"

# Cross validate our classifier. Calculate the accuracy using K-Folds technique
def cross_validate(data):
	k_fold = KFold(n=len(data), n_folds=NO_OF_FOLDS)
	scores = []

	for train_indices, test_indices in k_fold:
		train_text = data.iloc[train_indices]['text'].values
		train_y = data.iloc[train_indices]['user'].values

		test_text = data.iloc[test_indices]['text'].values
		test_y = data.iloc[test_indices]['user'].values

		pipeline.fit(train_text, train_y)
		predictions = pipeline.predict(test_text)

		score = accuracy_score(test_y, predictions)
		scores.append(score)

	print 'Total chats classified:', len(data)
	print 'Accuracy Score:', sum(scores)/len(scores)

if __name__ == "__main__":
	if len(sys.argv) == 4:
		raw_data = read_db_data(sys.argv[1], sys.argv[2], sys.argv[3])

		data_frame = build_data_frame(raw_data)

		train_classifier(data_frame)

		run_predictions(["Replace this with sample texts", "That you want to predict author for"])

		cross_validate(data_frame)
	else:
		print "Usage: compute_stats.py <group_name> <db_name> <collection_name>"