#!/bin/bash
#SBATCH -n 8                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 0-01:00              # Runtime in D-HH:MM
#SBATCH -p serial_requeue      	# Partition to submit to
#SBATCH --mem-per-cpu=1000  # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o ./logs/provR%j.out      # File to which STDERR will be written
#SBATCH -e ./logs/provR%j.err      # File to which STDERR will be written

# tell odyssey where to look for R libraries
export R_LIBS_USER=$HOME/apps/R:$R_LIBS_USER

# echo the doi to the error file
echo $2 >&2

doi_direct="$1/$2"

# suppress R output by redirecting to /dev/null
echo "Attempting to run and generate data provenance for raw R scripts in dataset..."
Rscript --default-packages=methods,datasets,utils,grDevices,graphics,stats \
	get_dataset_provenance.R $doi_direct "n" &> /dev/null

echo "Preprocessing library loads for the dataset..."
python preprocess_r_scripts.py $doi_direct

# suppress R output by redirecting to /dev/null
echo "Attempting to run and generate data provenance for pre-processed R scripts in dataset..."
Rscript --default-packages=methods,datasets,utils,grDevices,graphics,stats \
	get_dataset_provenance.R $doi_direct "y" &> /dev/null
