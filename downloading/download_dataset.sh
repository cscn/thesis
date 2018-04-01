#!/bin/bash
#SBATCH -n 8                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 0-01:00              # Runtime in D-HH:MM
#SBATCH -p serial_requeue      	# Partition to submit to
#SBATCH --mem-per-cpu=1000  # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o ./logs/doi_download%j.out      # File to which STDERR will be written
#SBATCH -e ./logs/doi_download%j.err      # File to which STDERR will be written

# echo "Downloading dataset corresponding to DOI: $1..."
echo $1 >&2
doi_direct=$(python download_dataset.py $1 $2)