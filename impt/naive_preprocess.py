import sys
import os
from helpers import convert_r_files, all_preproc

# get the directory name as command line argument
doi_direct = sys.argv[len(sys.argv) - 1]

# read in the run log
run_log = pd.read_csv(doi_direct + "/prov_data/run_log.csv")
# get filenames to preprocess
orig_files = [my_file for my_file in os.listdir(doi_direct) if\
			  my_file.endswith(".R") or my_file.endswith(".r")]
convert_r_files(doi_direct, replace=True)

# for each file that ran
for orig_file in orig_files:
	all_preproc(orig_file, doi_direct)