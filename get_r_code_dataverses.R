# load module dependencies
library(dataverse)
library(stringr)
# environmental variables required by dataverse
Sys.setenv("DATAVERSE_KEY" = "670994aa-dbf5-4240-a3a6-74cca05a9f07")
Sys.setenv("DATAVERSE_SERVER" = "dataverse.harvard.edu")

# detect the total number of R files in all dataverses
# we want to record the number of .R files so we know how many pages of metadata to receive
# first we need to capture Y from the console message "X of Y results retrieved"
captured_message = capture.output(query_result = dataverse_search("*.R" ,type="file")$name, type="message")

# use regex (with stringr module) to parse out the number of files and convert to integer
num_files = as.numeric(str_extract_all(captured_message, "[0-9]+")[[1]][2])

# initialize empty dataframe
r_dataverse = data.frame(doi=c("foo"), citation=c("bar"), stringsAsFactors = FALSE)

# store DOI and citation for all R files
# for all pages of .R files
for (i in 0:ceiling(num_files/20)) {
  # get the ith page of .R files
  rfiles = dataverse_search("*.R", type="file", start=i, per_page=20)
  # iterate through the citations
  for (citation in rfiles$dataset_citation) {
    # parse out the doi
    citation_doi = str_extract(citation, "doi[^,]+")[[1]][1]
    # append doi and citation to dataframe
    r_dataverse = rbind(r_dataverse, list(citation_doi, citation))
  } 
}

# save csv just in case
write.csv(r_dataverse, file="dataverse_doi.csv")

# remove whitespace, filter out duplicates, drop NAs
clean_r_dataverse$doi = as.character(str_trim(clean_r_dataverse$doi))
clean_r_dataverse = unique(clean_r_dataverse)
clean_r_dataverse = na.omit(clean_r_dataverse)
# remove the first row (junk values used for initializing the dataframe)
clean_r_dataverse = clean_r_dataverse[-1,]

# save csv of cleaned dois
write.csv(clean_r_dataverse, file="dataverse_doi_clean.csv")

# get lists of ids and filenames for all files in first couple dataverses as an example
doi_fileids = data.frame(doi = c("foo"), id = c("bar"), filename = c("baz"), 
                         stringsAsFactors = FALSE)
for (i in c(1:4)) {
  # get ith doi from list
  curr_doi = clean_r_dataverse$doi[i]
  # request metadata about current dataverse from Dataverse API; filter for the relevant information
  curr_files = get_dataset(curr_doi)[13]$files
  # append current dataverse (doi)'s filenames and file ids to the dataframe as a single row,
  # concatenating filenams and ids into single strings separated by commas for easy appending
  doi_fileids = rbind(doi_fileids, c(curr_doi, paste(curr_files$id, collapse=","), 
                                     paste(curr_files$filename, collapse=",")))
}
# remove the placeholders used to initialize the dataframe (foo, bar, baz)
doi_fileids = doi_fileids[-1,]

# write doi to filename/id mappings to csv
write.csv(doi_fileids, file="r_dataverse_ids.csv")
