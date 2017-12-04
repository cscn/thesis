# load dataverse module and set relevant system variables
library(dataverse)
Sys.setenv("DATAVERSE_KEY" = "670994aa-dbf5-4240-a3a6-74cca05a9f07")
Sys.setenv("DATAVERSE_SERVER" = "dataverse.harvard.edu")

# 

# trying out a dataverse search for all .R files
rfiles = dataverse_search("*.R" ,type="file")
names(rfiles)
# useful part of each search result, containing doi
rfiles[1,]$dataset_citation

# get the number of R files to capture
captured_output = capture.output(query_result = dataverse_search("*.R" ,type="file")$name, type="message")

# query dataverse for .R files
for (i in c(1:length(rfiles[,1]))) {
  cat(rfiles[i,]$dataset_citation, "\n")
}