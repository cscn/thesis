import os
import sys

import pandas as pd

from helpers import get_runlog_data, get_missing_files

# accept commandline arguments for dataset directory and 
# output directory for the resultant csv
output_direct = sys.argv[-1]
dataset_direct = sys.argv[-2]
run_log_df, error_files = get_runlog_data(dataset_direct)

# make a new directory to store the dataset
# (if one doesn't exist)
if not os.path.exists(output_direct):   
	os.makedirs(output_direct)

# write the dataframe to csv
run_log_df.to_csv(output_direct + '/master_run_log.csv', index=False)

# create a pickle of missing files
get_missing_files(dataset_direct, output_direct)

# if there were errors, write those to the directory as well
if error_files:
	with open(output_direct + 'error_files.txt', 'w') as handle:
		for error_file in error_files:
			handle.write(error_file + '\n')