# get commandline arguments
args = commandArgs(trailingOnly=TRUE)
# parse command line args for path to the directory and DOI
dir_path_doi = args[1] # example: "doi--10.7910-DVN-26905"

# set the working directory to the dataset directory
setwd(dir_path_doi)
library(stringr)
library(provR)
# create directory to store provenance data
dir.create("prov_data", showWarnings = FALSE)

# initialize dataframe to store results of attempting to run 
# (and collect provenance on) the script
run_log = data.frame(doi = c("foo"), filename = c("bar"), run_type = c("bazz"),
					 error = c("fizz"), stringsAsFactors = FALSE)
run_log = run_log[-1,]
# open the run log for writing
write.csv(run_log, file="prov_data/run_log.csv", row.names=FALSE)

# get list of preprocessed R files in dataset
r_files = list.files(".", pattern="_preproc\\.R\\>", recursive=FALSE, full.names=FALSE)

# for each R file
for (r_file in r_files) {
	# parse out file name, leaving out the ".R" part
	filename = substr(r_file, 1, nchar(r_file) - 2)
	for (run_type in c("source", "provR")) {
		# save local variables in case the script clears the workspace
		save(run_type, dir_path_doi, r_files, r_file, filename,
			 file="prov_data/get_prov.RData")
		if (run_type == "source") {
		# try to run the R file with error handling
			error = try(source(r_file), silent = TRUE)[1]
		}
		else {
			error = try(prov.capture(r_file), silent = TRUE)[1]
		}
		# restore local variables
		load("prov_data/get_prov.RData")
		# if there was no error
		if (is.null(error)) {
			error = NA
			# save the provenance if correct run_type
			if (run_type == "provR") {
				write(prov.json(), paste0("prov_data/", "prov_", filename, ".json"))
			}
		} 
		else {
			# trim whitespace from beginning and end of string
		    error = str_trim(error)
		    # parse all the quotes from the error string
		    error = str_replace_all(error, "\"", "")
		    # replace all newline characters in middle of string with special string
		    error = str_replace_all(error, "[\n]", "[newline]")
		}
		# create dataframe from doi, filename, run_type, and errors to facilitate csv writing
		new_log_data = data.frame(doi=c(dir_path_doi), filename=c(r_file),
								  run_type=c(run_type), error=c(error),
								  stringsAsFactors = FALSE)
		# write the new log data into the log file
		write.table(new_log_data, file="prov_data/run_log.csv", sep=",", append=TRUE,
					row.names=FALSE, col.names=FALSE)
	}
}
