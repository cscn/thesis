#!/bin/bash

echo "Downloading dataset corresponding to DOI: $1..."
doi_direct=$(python download_dataset.py $1 $2)

echo "Preprocessing library loads for the dataset..."
python preprocess_library_loads.py $doi_direct

# suppress R output by redirecting to /dev/null
echo "Attempting to run and generate data provenance for R scripts in dataset..."
Rscript --default-packages=methods,datasets,utils,grDevices,graphics,stats \
	get_dataset_provenance.R $doi_direct &> /dev/null