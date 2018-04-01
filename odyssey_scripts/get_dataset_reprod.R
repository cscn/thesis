##################################################
# Attempts to collect provenance data for each file, logging errors if necessary
# Command line arguments:
# dir_path_doi : string 
#				 path to the directory for which to run this script
# preproc : string
# 			either "y" or "n"
##################################################

# get commandline arguments
args = commandArgs(trailingOnly=TRUE)
# parse command line args for path to the directory and preprocessing
dir_path_doi = args[1] # example: "doi--10.7910-DVN-26905"
preproc = args[2] == "y" # preprocessing 

# set the working directory to the dataset directory
setwd(dir_path_doi)
library(stringr)
library(provR)

# create directory to store provenance data
dir.create("prov_data", showWarnings = FALSE)

# initialize dataframe to store results of attempting to run 
# (and collect provenance on) the script
if (!file.exists("prov_data/run_log.csv")) {
	run_log = data.frame(doi = c("foo"), filename = c("bar"), run_type = c("bazz"),
					 error = c("fizz"), stringsAsFactors = FALSE)
	run_log = run_log[-1,]
	# initialize the csv with proper column names
	write.csv(run_log, file="prov_data/run_log.csv", row.names=FALSE)
}

# get correct list of r files to run the script on depending on commandline args
if (preproc) {
	r_files = list.files(".", pattern="__preproc__\\.[Rr]\\>", recursive=FALSE, full.names=FALSE)
} else {
	r_files = list.files(".", pattern="\\.[Rr]\\>", recursive=FALSE, full.names=FALSE)
	# parse out preprocessed files
	preproc_files = grep("_preproc", r_files)
	if (length(preproc_files) > 0) {
		r_files = r_files[-preproc_files]
	}
}
# for each R file
for (run_type in c("source", "provR")) {
	for (r_file in r_files) {
		# parse out file name, leaving out the ".R" part
		filename = substr(r_file, 1, nchar(r_file) - 2)
		# save local variables in case the script clears the workspace
		save(run_type, dir_path_doi, r_files, r_file, filename,
			 file="prov_data/get_reprod.RData")
		if (run_type == "source") {
		# try to run the R file with error handling
			error = try(source(r_file), silent = TRUE)
		}
		else {
			error = try(prov.capture(r_file), silent = TRUE)
		}
		# restore local variables
		load("prov_data/get_reprod.RData")
		# if there was an error
		if (class(error) == "try-error") {
			# trim whitespace from beginning and end of string
		    error = str_trim(error[1])
		    # parse all the quotes from the error string
		    error = str_replace_all(error, "\"", "")
		    # replace all newline characters in middle of string with special string
		    error = str_replace_all(error, "[\n]", "[newline]")
		}
		else {
			error = "success"
			# save the provenance if correct run_type
			if (run_type == "provR") {
				write(prov.json(), paste0("prov_data/", "prov_", filename, ".json"))
			}
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
