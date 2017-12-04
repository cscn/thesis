# load dataverse module and set relevant system variables
library(dataverse)
Sys.setenv("DATAVERSE_KEY" = "670994aa-dbf5-4240-a3a6-74cca05a9f07")
Sys.setenv("DATAVERSE_SERVER" = "dataverse.harvard.edu")

# trying out a dataverse search for all .R files
rfiles = dataverse_search("*.R" ,type="file")
names(rfiles)


# trying out a dataverse search for .R files
rfiles = dataverse_search("*.R", type="file")
names(rfiles)

# We can get any page of results with the "start" parameter (0-indexed). 
# This should generate the same result as the above line
rfiles1 = dataverse_search("*.R", type="file", start=0)
setdiff(rfiles, rfiles1) # has no output if they are truly equal

# we want to record the number of .R files so we know how many pages of metadata to receive
# first we need to capture Y from the console message "X of Y results retrieved"
captured_message = capture.output(query_result = dataverse_search("*.R" ,type="file")$name, type="message")

# use regex (with stringr module) to parse out the number of files and convert to integer
num_files = as.numeric(str_extract_all(captured_message, "[0-9]+")[[1]][2])
num_files

# query dataverse for .R files
for (i in c(1:length(rfiles[,1]))) {
  cat(rfiles[i,]$dataset_citation, "\n")
}