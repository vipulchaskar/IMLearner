#Parse input file from whatsapp email export

import re
import sys
from pymongo import MongoClient


# Input file to read whatsapp data from
# chat_file = "chat_sample.txt"
# List of keywords to exclude from data. If one of the following keyword is found in a message,
# That message is excluded. Used to remove uninformative messages such as media.
exclude_texts = ["<Media omitted>", ""]

# RegEx used to interpret structure of a whatsapp chat history from email.
# First group is timestamp, second the name of sender and third is the actual message.
wa_regex = re.compile('(.*?) - (.*?): (.*)')
# Regex used to match for the timestamp format of whatsapp chat history.
wa_time_regex = re.compile('\d+/\d+/\d+, \d+:\d+ .*- ')

FORWARD_THRESHOLD = 5

def pretty_print(data):
	print data['timestamp'], ":", data['user'], ":", data['text']

def initializeMongo(db_name, collection_name):
	client = MongoClient()
	db = client[db_name]
	collection = db[collection_name]
	return collection

def create_document(collection, doc):
	# Create a mongodb document and add to the collection 'raw_text'
	# Check for the presence of excluded keywords. Don't add a message if keyword present
	if doc['text'] not in exclude_texts:
		collection.insert(doc)

def purge_cache(cache, collection):
	# Handle the existing cache. Write to database only if previous user had sent less than
	# FORWARD_THRESHOLD lines. Because more than FORWARD_THRESHOLD consequtive lines from
	# the same user means that he/she sent a forward. We don't want to consider that.
	if len(cache) != 0 and len(cache) <= FORWARD_THRESHOLD:
		for doc in cache:
				create_document(collection, doc)

	return []

def parse_and_dump(chat_file, group_name, db_name, collection_name):
	# Intialize database
	collection = initializeMongo(db_name, collection_name)

	# Delete existing entries
	collection.remove({})

	# Open the file to parse
	with open(chat_file,'r') as inputfile:

		last_user = ""
		last_timestamp = ""
		cache = []

		for line in inputfile:

			text = ""

			split_line = wa_regex.match(line)

			if split_line:          # If beginning of msgs from a user,

				cache = purge_cache(cache, collection)

				# Record the details of current user
				last_user = split_line.group(2)
				last_timestamp = split_line.group(1)
				text = split_line.group(3)

			# When a user sends multiple consequtive messages, his 2nd onwards messages will not contain
			# timestamp or name. In this case, assign those messages with his name picked up from his 1st message
			elif not wa_time_regex.match(line):
				text = line.strip()

			# Create a dictionary to hold mongodb document of current msg
			doc = {}
			doc['user'] = last_user
			doc['timestamp'] = last_timestamp
			doc['text'] = text
			doc['group'] = group_name

			cache.append(doc)

		# Handle the case where we have parsed the whole file and there are some msgs in cache which
		# haven't been written to the db yet.
		cache = purge_cache(cache, collection)


if __name__ == "__main__":
	if len(sys.argv) == 5:
		parse_and_dump(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print "Usage : python parse_input.py <chat_file> <group_name> <db_name> <collection_name>"
