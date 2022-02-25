#!/bin/bash

for dir in $(find data -mindepth 1 -maxdepth 1 -type d); do
	echo -n "Removing the directory ${dir} ... "

	if rm -r "${dir}"; then
		echo "DONE"
	else
		echo "Unable to delete '${dir}'!"
	fi
done