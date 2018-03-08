import requests
import json
import re
import os
import shutil
import fnmatch

import pandas as pd
import numpy as np

def doi_to_directory(doi):
	"""Converts a doi string to a more directory-friendly name
	Parameters
	----------
	doi : string
		  doi
	
	Returns
	-------
	doi : string
		  doi with "/" and ":" replaced by "-" and "--" respectively
	"""
	return doi.replace("/", "-").replace(":", "--")

def directory_to_doi(doi):
	"""Converts a doi string to a more directory-friendly name
	Parameters
	----------
	doi : string
		  doi
	
	Returns
	-------
	doi : string
		  doi with "-" and "--" replaced by "/" and ":" respectively
	"""
	return doi.replace("--", ":").replace("-", "/")

def get_r_dois(dataverse_key, save=False, print_status=False,
			   api_url="https://dataverse.harvard.edu/api/search/"):
	"""Get list of dois for all R files in a dataverse (defaulting to Harvard's)
	Parameters
	----------
	dataverse_key : string 
					containing user's dataverse API key
	save : boolean
		   whether or not to save the result as a .txt file
	print_status : boolean
				   whether or not to print status messages
	api_url : string
			  url pointing to the dataverse to get URLs for
	Returns
	-------
	r_dois : list of string
			 dois containing r_files in Harvard dataverse
	"""
	# defining some constants
	r_file_query = "fileContentType:type/x-r-syntax"

	# initialize variables to store current state of scraping
	page_num = 0
	r_dois = []

	#  keep requesting until the API returns fewer than 1000 results
	while True:
		if print_status:
			print("Requesting page {} from API...".format(page_num))
		# query the API for 1000 results
		myresults = requests.get(api_url,
								 params= {"q": r_file_query, "type": "file",
								 "key": dataverse_key,
								 "start": str(1000 * page_num),
								 "per_page": str(1000)}).json()['data']['items']

		if print_status:
			print("Parsing results from page {}...".format(page_num))
		
		# iterate through results, recording dataset_citations
		for myresult in myresults:
			# extract the DOI (if any) from the result
			doi_match = re.search("(doi:[^,]*)", myresult['dataset_citation'])
			if doi_match:
				r_dois.append(doi_match.group(1) + '\n')

		# if fewer than 1000 results were returned; we must have reached the end
		if len(myresults) < 1000:
			if print_status:
				print("Reached last page of results. Done.")
			break
		page_num += 1

	# remove duplicate DOIs
	r_dois = list(set(r_dois))

	# if save, then save as .txt file 
	if save:
		# remove old output file if one exists
		if os.path.exists('r_dois.txt'):   
			os.remove('r_dois.txt')

		# write dois to file, one-per-line
		with open('r_dois.txt', 'a') as myfile:
			map(myfile.write, r_dois)
	return r_dois

def get_runlog_data(path_to_datasets):
	"""Aggregate run-time data for all datasets in the given
	Parameters
	----------
	path_to_datasets : string 
					   path to the directory containing processed datasets
	Returns
	-------
	(run_data_df, error_dois) : tuple of (pandas.DataFrame, list of string)
								a tuple containing a pandas DataFrame with the 
								aggregated results of attempting to run the R code
								in all the datasets, followed by a list of datasets
								for which aggregating the results failed (should be
								an empty list unless there was a catastrophic error)
	
	"""
	# get list of dataset directories, ignoring macOS directory metadata file (if present)
	doi_directs = [doi for doi in os.listdir(path_to_datasets) if doi != '.DS_Store']
	# initialize empty dataframe to store run logs of all the files
	run_data_df = pd.DataFrame()
	# initialize empty list to store problem doi's
	error_dois = []

	# iterate through directories and concatenate run logs
	for my_doi in doi_directs:
		try:
			# assemble path
			my_path = path_to_datasets + '/' + my_doi + '/prov_data/' + 'run_log.csv'
			# concatenate to dataframe
			run_data_df = pd.concat([run_data_df, pd.read_csv(my_path)])
		except:
			error_dois.append(my_doi)
	return (run_data_df, error_dois)

def refresh_datasets(path_to_datasets):
	"""Clean datasets of all traces of preprocessing and provenance collection
	Parameters
	----------
	path_to_datasets : string 
					   path to the directory containing processed datasets
	"""
	# get list of dataset directories, ignoring macOS directory metadata file (if present)
	doi_directs = [doi for doi in os.listdir(path_to_datasets) if doi != '.DS_Store']

	# iterate through directories, deleting prov_data directory and preprocessed files
	for my_doi in doi_directs:
		# assemble paths
		doi_dir_path = path_to_datasets + '/' + my_doi
		# get list of ignoring macOS directory metadata file (if present)
		doi_files = [my_file for my_file in os.listdir(doi_dir_path) if\
					 my_file != '.DS_Store' and re.match('.*_preproc0', my_file)]
		# remove preprocessed files
		for my_file in doi_files:
			doi_file_path = doi_dir_path + '/' + my_file
			try: 
				os.remove(doi_file_path)
			except OSError:
				pass
		# remove prov_data directory
		try:
			shutil.rmtree(doi_dir_path + '/prov_data')
		except:
			pass

def find_file(pattern, path):
	"""Recursively search the directory pointed to by path for a file matching pattern.
	   Inspired by https://stackoverflow.com/questions/120656/directory-listing-in-python
	Parameters
	----------
	pattern : string
			  unix-style pattern to attempt to match to a file
	path : string
		   path to the directory to search

	Returns 
	-------
	string 
	path to a matching file or the empty string
	"""
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name, pattern):
				return os.path.join(root, name)
	return ''

def find_dir(pattern, path):
	"""Recursively search the directory pointed to by path for a directory matching pattern.
	   Inspired by https://stackoverflow.com/questions/120656/directory-listing-in-python
	Parameters
	----------
	pattern : string
			  unix-style pattern to attempt to match to a directory
	path : string
		   path to the directory to search

	Returns 
	-------
	string 
	path to a matching directory or the empty string
	"""
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)
    return ''