import sys
import os
import shutil
import re

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
					 my_file != '.DS_Store' and re.match('.*__preproc__', my_file)]
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

# accept commandline arguments for dataset directory
dataset_direct = sys.argv[-1]

# prompt the user for confirmation
are_you_sure = raw_input("Are you sure you want to delete provenance and execution logs for " +
						 dataset_direct + "? (yes/no) ")
if are_you_sure == "yes":
	refresh_datasets(dataset_direct)
