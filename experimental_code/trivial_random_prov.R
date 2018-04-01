# update ProvR
library(devtools)
install_github("ProvTools/ProvR")

# set the correct working directory
setwd("/Users/chrischen/thesis_repo")

# helper function to unmount a package from 
# stackoverflow: https://stackoverflow.com/questions/6979917/how-to-unload-a-package-without-restarting-r
detach_package <- function(pkg, character.only = FALSE) {
  if(!character.only) {
    pkg <- deparse(substitute(pkg))
  }
  search_item <- paste("package", pkg, sep = ":")
  while(search_item %in% search()) {
    detach(search_item, unload = TRUE, character.only = TRUE)
  }
}
  
##### RDataTracker syntax #####
detach_package(provR)
library(RDataTracker)
RDataTracker::ddg.set.detail(3)
RDataTracker::ddg.get.detail()
RDataTracker::ddg.run("trivial_randomness.R", max.loops=100, annotate.inside=TRUE)

##### ProvR syntax #####
# make sure there's no interference from RDataTracker dependencies
detach_package(RDataTracker)
library(provR)
success = try(prov.capture("trivial_randomness.R"), silent = T)[1]
if (is.null(success)) {
  dir.create("dataverse_provenance")
  write(prov.json(), paste0("dataverse_provenance/", "prov_", "trivial_randomness.json"))
}

