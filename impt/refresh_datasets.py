from helpers import refresh_datasets

# accept commandline arguments for dataset directory
dataset_direct = sys.argv[:-1]
refresh_datasets(dataset_direct)
