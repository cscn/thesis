import sys
import os
from helpers import convert_r_files, all_preproc

# get the directory name as command line argument
dataset_dir = sys.argv[len(sys.argv) - 1]
for dataset in os.listdir(dataset_dir):
    if dataset.startswith("doi"):
        dataset_path = os.path.join(dataset_dir, dataset)
        # get filenames to preprocess
        orig_files = [my_file for my_file in os.listdir(dataset_path) if\
                      my_file.endswith(".R") or my_file.endswith(".r") and\
                      "__preproc__" not in my_file]

        convert_r_files(dataset_path, replace=True)

        # for each file that ran
        for orig_file in orig_files:
            all_preproc(orig_file, dataset_path, "error")