"""
Download datasets containing R files from Harvard Dataverse
By: Chris Chen
Email: cchen02@college.harvard.edu
Signaling implementation taken from 
https://stackoverflow.com/questions/25027122/break-the-function-after-certain-time
"""

import pickle
import requests
import json
import os
import signal
import shutil

from tqdm import tqdm as tqdm

dataverse_key = "670994aa-dbf5-4240-a3a6-74cca05a9f07"

class TimeoutException(Exception):   # Custom exception class
	pass

def timeout_handler(signum, frame):   # Custom signal handler
	raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

# make a doi a friendlier for a directory name
def doi_to_direct(doi_string):
	return doi_string.replace("/", "-").replace(":", "--")

# load the dictionary from pickle
with open('doi_to_fileids.pkl', 'rb') as handle:
	doi_to_fileids = pickle.load(handle)

# convert the dictionary to a list of key/value pairs and 
# free the dictionary from ram
my_items = doi_to_fileids.items()

# iterate through the key/value pairs in the dictionary
for i in tqdm(range(len(my_items))):
	# start the timer. Once 30 seconds are over, a SIGALRM signal is sent.
	signal.alarm(60)
	# Catch TimeoutException when it's sent.
	try:
		mydoi, myfile_tuples = my_items[i]
		# make the DOI a friendly directory name 
		mydirect = 'Rdatasets/' + doi_to_direct(mydoi)
		# if the dataset does not have a directory, create it
		if not os.path.exists(mydirect):   
			os.makedirs(mydirect)
		# iterate through list of filename, fileid tuples
		for filename, fileid in myfile_tuples:
			response = requests.get("https://dataverse.harvard.edu/api/access/datafile/" + str(fileid), 
									params={"key": dataverse_key})
			# write the response to a new file with the correct filename
			with open(mydirect + "/" + filename, 'w') as handle:
				handle.write(response.content)
	except TimeoutException:
		# cleanup the directory
		shutil.rmtree(mydirect)
		continue # continue the for loop if downloading takes more than 30 seconds
	else:
		# Reset the alarm
		signal.alarm(0)