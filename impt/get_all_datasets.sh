#!/bin/bash

file="$1"
while read -r doi
do
	sbatch ./get_prov_for_doi.sh $doi
	sleep 5 
done < "$file"
