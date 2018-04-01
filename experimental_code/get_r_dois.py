import requests
import json
import re
import os

# defining some constants
r_file_query = "fileContentType:type/x-r-syntax"
dataverse_key = "3b0777ab-4af9-4b3a-971e-5c84ac75926b"

# initialize variables to store current state of scraping
page_num = 0
r_dois = []
#  keep requesting until the API returns fewer than 1000 results
while True:
	print("Requesting page {} from API...".format(page_num))
	# query the API for 1000 results
	myresults = requests.get("https://dataverse.harvard.edu/api/search/",
							 params= {"q": r_file_query, "type": "file",
							 "key": dataverse_key,
							 "start": str(1000 * page_num),
							 "per_page": str(1000)}).json()['data']['items']

	print("Parsing results from page {}...".format(page_num))
	
	# iterate through results, recording dataset_citations
	for myresult in myresults:
		# extract the DOI (if any) from the result
		doi_match = re.search("(doi:[^,]*)", myresult['dataset_citation'])
		if doi_match:
			r_dois.append(doi_match.group(1) + '\n')

	# if fewer than 1000 results were returned; we must have reached the end
	if len(myresults) < 1000:
		print("Reached last page of results. Done.")
		break
	page_num += 1

# remove duplicate DOIs
r_dois = list(set(r_dois))

# remove old output file if one exists
if os.path.exists('r_dois.txt'):   
	os.remove('r_dois.txt')

# write dois to file, one-per-line
with open('r_dois.txt', 'a') as myfile:
	map(myfile.write, r_dois) 