import sys
import os
import shutil
import re

from helpers import refresh_datasets

# accept commandline arguments for dataset directory
dataset_direct = sys.argv[-2]
archive_direct = sys.argv[-1]

refresh_datasets(dataset_direct, archive_direct)
