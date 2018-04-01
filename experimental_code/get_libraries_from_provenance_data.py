import json # for reading files
import re # for parsing the library strings

# read in JSON file
path = "/Users/chrischen/Dropbox/Harvard/Fall '17/thesis/r_test_files/hw4_ddg/ddg.json"

# iterate through JSON
with open(path, 'r') as infile:
	prov_json = json.load(infile)["activity"]

# regular expression to capture library name
library_regex = re.compile(r"library\((?P<lib_name>.*)\)", re.VERBOSE)

# set of used libraries
used_libraries = set()

# Identify libraries being used in script and add them to set
for key in prov_json:
	if "rdt:name" in prov_json[key]:
		lib_name = library_regex.match(prov_json[key]["rdt:name"])
		if lib_name:
			used_libraries.add(str(lib_name.group("lib_name")))

# Filter packages in user's environment by which ones were used
for package_dict in prov_json["environment"]["rdt:installedPackages"]:
	if package_dict["package"] in used_libraries:
		print package_dict


			

