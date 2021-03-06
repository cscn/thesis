import os
import re

import pandas as pd
import numpy as np

# load paths for provenance collection
prov_paths = pd.read_csv("prov_paths.csv")
# filter for only R files
prov_paths = prov_paths[prov_paths["filename"].str.contains("\.R")]

# iterate through the number of rows in prov_paths
for row_num in range(prov_paths.shape[0]):
	# parse out R file metadata
	myrow = prov_paths.iloc[row_num]
	mydoi = myrow["doi"]
	myfile = myrow["filename"]
	mywd = myrow["wd"]
	try:
		# parse out filename and construct file paths
		filename = myfile.split(".R")[0]
		file_path = mywd + "/" + myfile
		# path to preprocessed file, named with suffix "_preproc"
		preproc_path = mywd + "/" + filename + "_preproc" + ".R"
		# path to temp file, named with suffix "_temp"
		temp_path = mywd + "/" + filename + "_temp" + ".R"

		# replace library, require, and install.packages calls with "install_and_load"
		with open(file_path, 'r') as infile:
			with open(temp_path, 'w') as outfile:
				# for each line in the input file
				for line in infile.readlines():
					# replace "library" calls
					library_replace = re.sub("library\((.*)\)", "install_and_load(\"\\1\")", line)
					# replace "require" calls
					require_replace = re.sub("require\((.*)\)", "install_and_load(\"\\1\")", library_replace)
					# replace "install.packages" calls
					install_replace = re.sub("install.packages\((.*)\)", "install_and_load(\\1)", require_replace)
					# write the result to a temporary file
					outfile.write(install_replace)

		# wipe the preprocessed file and open it for writing
		open(preproc_path, 'w').close()
		with open(preproc_path, 'a+') as outfile:
			# add in declaration for "install_and_load" at the head of the preprocessed file
			with open("install_and_load.R", 'r') as infile:
				map(outfile.write, infile.readlines())
			# append modified code from .R file
			with open(temp_path, 'r') as infile:
				for line in infile.readlines():
					outfile.write(line)
					# if the line clears the environment, re-declare "install_and_load" immediately after
					if "rm(" in line:
						with open("install_and_load.R", 'r') as install_and_load:
							map(outfile.write, install_and_load.readlines())   

		# delete the temporary file
		os.remove(temp_path)
	except:
		print "Failure on Row Number {}: {} {}; {}".format(row_num,
														   mydoi,
														   myfile,
														   mywd)

	# progress messages
	if row_num % 100 == 0:
		print "Done with {} of {}".format(row_num, prov_paths.shape[0])