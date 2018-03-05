import sys
from helpers import refresh_datasets

# accept commandline arguments for dataset directory
dataset_direct = sys.argv[-1]

# prompt the user for confirmation
are_you_sure = raw_input("Are you sure you want to delete provenance and execution logs for " +
						 dataset_direct + "? (yes/no) ")
if are_you_sure == "yes":
	refresh_datasets(dataset_direct)
