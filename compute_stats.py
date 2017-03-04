# Read data from mongo and perform some statistical analysis

from pymongo import MongoClient
import matplotlib.pyplot as plt
import sys

freq_data = {}
freq_time_data = {k:{} for k in range(24)}

def initializeMongo(db_name, collection_name):
	client = MongoClient()
	db = client[db_name]
	collection = db[collection_name]
	return collection

def read_and_compute_stats(group_name, db_name, collection_name):

	collection = initializeMongo(db_name, collection_name)

	# Show the frequency of each user's messages
	freq_data_mongo = collection.aggregate([{ '$group' : { '_id' : '$user', 'count': {'$sum' : 1}}}])
	for record in freq_data_mongo:
		freq_data[record['_id']] = record['count']

	plt.bar(range(len(freq_data)), freq_data.values(), align='center')
	plt.xticks(range(len(freq_data)), freq_data.keys())
	plt.show()

	#for document in collection.aggregate([{"$group": {"_id": "$user"}}]):
	#	freq_time_data2 = {k:v.update({document['_id']:""}) for k,v in freq_time_data}

	


if __name__ == "__main__":
	if len(sys.argv) == 4:
		read_and_compute_stats(sys.argv[1], sys.argv[2], sys.argv[3])
	else:
		print "Usage: compute_stats.py <group_name> <db_name> <collection_name>"