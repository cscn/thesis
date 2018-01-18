#!/bin/bash

### The first trailing argument shold be the output file name
touch $1

### use: sh mash_batch.sh <sketch directory> <sketch directory>  <output file name> 

for i in $(ls | grep SM); do
    for j in $(ls | grep SM); do 
	echo $i $j
	sbatch ../bin/run_mash.sh $i $j $1
	sleep 5
    done
done

say "Mash just finished deploying"
