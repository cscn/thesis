#!/bin/bash

file="$1"
while read -r doi
do
	sbatch ./download_dataset.sh $doi $2
	sleep 5 
done < "$file"
