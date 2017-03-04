# README #

NOTE: This is a work in progress.

A Machine Learning (supervised classification) application which learns from the training data of whatsapp chat history, and given a message from some unknown user, predicts which user must have sent that message.

### TODO ###

* Handle the case where a user sends a forwarded message. We do not want to consider that as part of our data.
* Show the unique users after data is scanned. Such that messages from the same user with different names can be taken care of.

### Current implementation ###

* Bag of words technique for feature vectorization (Count Vectorizer with n-grams of range 1-5)
* Classification Algorithm - Stochastic Gradient Descent

### Current testing ###

* Training data - 9570 messages from 8 unique users
* Accuracy from K-Fold (K=6) method ~ 40.57%  :(

### Possible improvements ###

* Other Naive Bayes implementations (like Bernoulli)
* Use N-grams
* Try SVMs (sklearn.linear_model.SGDClassifier) ?
* TF-IDF transforms?
* Create and analyze confusion matrix

### Possible features in case feature extraction has to be done manually ###

* Number of words in message
* Number of consecutive emojis in message
* Type of emojis entered
* Message endings
* Number of non-dictionary words
* Number of capitalized words
* Total number of messages sent by a person
* Non-alphabet characters in message
* Timing of the day when a user sends the message
* Vowel Frequency
* Consonant Frequency
* Digit Frequency
* Punctuation Frequency
* Spacing Frequency
* Special Character Frequency
* Word Count
* Characters Per Word
* Words Per sentence
* Preposition Frequency
* Pronoun Frequency
* Determiner Frequency
* Conjunction Frequency
* Attribution Frequency
* Link Frequency
* 1 Letter Word
* 2 Letter Word
* 3 Letter Word
* 4 Letter Word
* 5 Letter Word
* 6 Letter Word
* 7 Letter Word
* 8-10 Letter Word
* 11-20 Letter Word

Please refer : https://www.quora.com/Anonymity-Quora-feature/How-vulnerable-are-Quora-answers-to-automated-writing-style-analysis


### References ###

* http://zacstewart.com/2015/04/28/document-classification-with-scikit-learn.html

* http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
