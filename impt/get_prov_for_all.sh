#!/bin/bash

file="$1"
while read -r doi
do
	sbatch ./get_prov_for_doi.sh $2 $doi
	sleep 1
done < "$file"
