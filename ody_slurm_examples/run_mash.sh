#!/bin/bash
#SBATCH -n 8                    # Number of cores
#SBATCH -N 1                    # Ensure that all cores are on one machine
#SBATCH -t 0-24:00              # Runtime in D-HH:MM
#SBATCH -p serial_requeue       # Partition to submit to
#SBATCH --mem-per-cpu=10000               # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o mash%j.out      # File to which STDERR will be written
#SBATCH -e mash%j.err      # File to which STDERR will be written
#SBATCH --mail-type=ALL         # Type of email notification- BEGIN,END,FAIL,ALL
#SBATCH --mail-user=matthewklau@fas.harvard.edu # Email to which notifications will be sent

### use: sh mash_batch.sh <sketch directory> <output file name> 

echo Mash starting $1 $2
../bin/mash dist $1/$1.fna.msh $2/$2.fna.msh >> $3
