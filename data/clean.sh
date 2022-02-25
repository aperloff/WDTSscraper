#!/bin/bash

while IFS= read -r -d '' dir
do
	echo -n "Removing the directory ${dir} ... "

	if rm -r "${dir}"; then
		echo "DONE"
	else
		echo "Unable to delete '${dir}'!"
	fi
done <  <(find data -mindepth 1 -maxdepth 1 -type d -print0)
