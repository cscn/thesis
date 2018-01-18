from __future__ import print_function

import requests
import json
import os
import sys
import pickle

# get DOI from command-line arguments
doi = sys.argv[len(sys.argv) - 2]
dataverse_key = sys.argv[len(sys.argv) - 1] # example: "670994aa-dbf5-4240-a3a6-74cca05a9f07"

# query the dataverse API for all the files in a dataverse
files = requests.get("https://dataverse.harvard.edu/api/datasets/:persistentId",
					 params= {"persistentId": doi, "key": dataverse_key})\
					 .json()['data']['latestVersion']['files']

# convert DOI into a friendly directory name by replacing slashes and colons
doi_direct = doi.replace("/", "-").replace(":", "--")

# make a new directory to store the files
if not os.path.exists(doi_direct):   
	os.makedirs(doi_direct)

# for each file result
for file in files:
	# parse the filename and fileid 
	filename = file['dataFile']['filename']
	fileid = file['dataFile']['id']

	# query the API for the file contents
	response = requests.get("https://dataverse.harvard.edu/api/access/datafile/" + str(fileid),
							params={"key": dataverse_key})

	# write the response to correctly-named file in the dataset directory
	with open(doi_direct + "/" + filename, 'w') as handle:
		handle.write(response.content)

# print out the dataset directory name for the shell script
print(doi_direct, end='')