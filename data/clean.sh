#!/bin/bash

for dir in `find data -mindepth 1 -maxdepth 1 -type d`; do
	echo -n "Removing the directory ${dir} ... "
	
	rm -r ${dir}
	
	if [[ "$?" == "0" ]]; then
		echo "DONE"
	else
		echo "Unable to delete '${dir}'!"
	fi
done