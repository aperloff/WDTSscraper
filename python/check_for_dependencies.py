#!/bin/env python3

import importlib
import pkg_resources
from shutil import which

pip_dependencies = {
	"pdfplumber" : [],
	"magiconfig" : [],
	"matplotlib" : [],
	"geopandas" : ["numpy", "pandas","shapely", "fiona", "pyproj", "rtree", "geoalchemy2", "geopy", "mapclassify", "matplotlib"],
}
try_dependencies = ["mpl_toolkits"]
system_dependencies = ["convert", "gs"] # 'convert' installed by ImageMagick

def is_tool(name):
	"""
	Check whether `name` is on PATH and marked as executable.

	Suggested from: https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
	"""
	return which(name) is not None

def check_for_dependencies():
	"""
	Suggested from: https://www.activestate.com/resources/quick-reads/how-to-list-installed-python-packages/
	"""
	installed_packages = pkg_resources.working_set
	installed_packages_versions_list = sorted([f"{i.key}=={i.version}" for i in installed_packages])
	installed_packages_list = sorted([f"{i.key}" for i in installed_packages])

	missing_pip = []
	for dependency, subdependencies in pip_dependencies.items():
		print(f"Checking for {dependency} ... ", end="")
		if dependency not in installed_packages_list:
			missing_pip.append(dependency)
			print("MISSING")
		else:
			print("FOUND")

		for subdependency in subdependencies:
			print(f"\tChecking for {subdependency} ... ", end="")
			if subdependency not in installed_packages_list:
				missing_pip.append(subdependency)
				print("MISSING")
			else:
				print("FOUND")

	missing_import = []
	for dependency in try_dependencies:
		print(f"Checking for {dependency} ... ", end="")
		try:
			importlib.import_module(dependency)
		except ImportError:
			missing_import.append(dependency)
			print("MISSING")
		else:
			print("FOUND")

	missing_system = []
	for dependency in system_dependencies:
		print(f"Checking for {dependency} ... ", end="")
		if not is_tool(dependency):
			missing_system.append(dependency)
			print("MISSING")
		else:
			print("FOUND")

	n_missing = len(missing_pip) + len(missing_import) + len(missing_system)
	if n_missing > 0:
		raise ModuleNotFoundError("There are missing dependencies!")
	else:
		print("\nAll dependencies installed!")

	return n_missing

if __name__ == "__main__":
	check_for_dependencies()