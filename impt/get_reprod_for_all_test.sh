#!/bin/bash

file="$1"
while read -r doi
do
	./get_reprod_for_doi_test.sh $2 $doi
	sleep 2
done < "$file"
