#!/bin/bash

directories=(
	"us_map"
	"schools"
	"CCI"
	"SCGSR"
	"SULI"
	"VFP")

# From: https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
us_map_location="https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_500k.zip"

# From: https://www.ed.gov/
# --> https://www2.ed.gov/rschstat/landing.jhtml?src=pn
# --> https://catalog.data.gov/dataset?organization=ed-gov
# --> https://catalog.data.gov/dataset?q=university&sort=views_recent+desc&organization=ed-gov&metadata_type=geospatial&as_sfid=AAAAAAVxgwGD0BppQSGW1W8qKBEZ23ZUneR7n84Ng4zHMjqPJiOqThubPZ80gfUna_LVwCWbLmcYfpZLGFuB5j3OKe78jh7hJAYj-SGhNruFavqaPNXsW5PvM4GZAw1IbIRsMO8%3D&as_fid=e0c896412e74e49c415df3d040221add0b7c1b35&ext_location=&ext_bbox=&ext_prev_extent=-141.6796875%2C8.754794702435618%2C-59.4140625%2C61.77312286453146
postsecondary_school_locations=("https://data-nces.opendata.arcgis.com/datasets/809cc7caddf34d3692970c9a781dac03_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2015 - 16
                                "https://data-nces.opendata.arcgis.com/datasets/72d9d1167cad4b619fa23f36f05e8766_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2016 - 17
                                "https://data-nces.opendata.arcgis.com/datasets/adc0c93f5b004246b186e90f4b43830f_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2017 - 18
                                "https://data-nces.opendata.arcgis.com/datasets/6aa17db388b34c6c9d6ae040993cd99d_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2018 - 19
                                "https://data-nces.opendata.arcgis.com/datasets/6a2b95d345d8452ca527b30490096391_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2019 - 20
                                "https://data-nces.opendata.arcgis.com/datasets/296839772bf14df29c290202f8547ff1_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D"  # 2020 - 21
                                "https://data-nces.opendata.arcgis.com/datasets/a15e8731a17a46aabc452ea607f172c0_0.zip?outSR=%7B%22latestWkid%22%3A4269%2C%22wkid%22%3A4269%7D") # Current

postsecondary_school_filenames=("Postsecondary_School_Locations_2015-16.zip"
								"Postsecondary_School_Locations_2016-17.zip"
								"Postsecondary_School_Locations_2017-18.zip"
								"Postsecondary_School_Locations_2018-19.zip"
								"Postsecondary_School_Locations_2019-20.zip"
								"Postsecondary_School_Locations_2020-21.zip"
								"Postsecondary_School_Locations_-_Current.zip")

# All From: https://science.osti.gov/wdts/CCI
cci_participants=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/2020-CCI-participants.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2019.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2018.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2017.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/2016-CCI-Terms_Participant-Report.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/2015-CCI-Terms_Participant-Report.pdf"
				  "https://science.osti.gov/-/media/wdts/cci/pdf/2014-CCI-Terms_Participant-Report.pdf")

# All From: https://science.osti.gov/wdts/scgsr/SCGSR-Awards
scgsr_participants=("https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2021-S1-Awards--public-announcement-SCGSRwebsite.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2020-S2-Awards--public-announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2020-Solicitation-1-Awards---Public-Annoucement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2019-Solicitation-2-SCGSR-Awards-Management---Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2019-Solicitation-1-SCGSR-Awards-Management-Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2018-Solicitation-2-SCGSR-Awards--Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2018-Solicitation-1-SCGSR-Awards--Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2017-Solicitation-2-Awards---Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2017-Solicitation-1-SCGSR-Awards-Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2016-Solicitation-2-SCGSR-Awards-Management-Public-Annoucement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2016-Solicitation-1-SCGSR-Awards-Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2015-Solicitation-2-SCGSR-Awards---Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/2015-Sol-1-SCGSR-Award-Public-Announcement.pdf"
					"https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2014-Awardee-Info1-External-Public.pdf")

# All From: https://science.osti.gov/wdts/suli
suli_participants=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/2020-SULI-participants.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2019.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2018_a.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2017.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/2016-SULI-Terms_Participant-Report.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/2015-SULI-Terms_Participant-Report.pdf"
				   "https://science.osti.gov/-/media/wdts/suli/pdf/2014-SULI-Terms_Participant-Report.pdf")

vfp_participants=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2020-VFP-F-participants.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2020-VFP-S-participants.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-F-participants-2019.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-S-participants-2019.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-F-participants-2018.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-S-participants-2018.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-F-participants-2017.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/VFP-S-participants-2017.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2016-VFP-Faculty-Terms_Participant-Report.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2016-VFP-Student-Terms_Participant-Report.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2015-VFP-Faculty-Terms_Participant-Report.pdf"
				  "https://science.osti.gov/-/media/wdts/vfp/pdf/2015-VFP-Student-Terms_Participant-Report.pdf")

for dir in "${directories[@]}"; do
	if [[ -d "data/${dir}" ]]; then
		echo "Directory data/${dir} already exists!"
	else
		echo -n "Creating the directory data/${dir} ... "
		mkdir "data/${dir}"
		echo "DONE"
	fi
done

download_command=""
if command -v curl &> /dev/null; then
	download_command="curl -O -s"
elif command -v wget &> /dev/null; then
	download_command="wget -q"
else
	echo "Uh oh! You don't have 'curl' or 'wget' available. Unable to download the input files."
fi

if [[ ! -z download_command ]]; then

	# Download the US map information
	echo -n "Downloading the US map information ... "
	cd data/us_map/
	eval "${download_command} ${us_map_location}"
	echo "DONE"

	echo -n "Extracting the US map shapefiles ... "
	for zip_file in `ls *.zip`; do
		unzip ${zip_file} > /dev/null
	done
	echo "DONE"	

	# Download the information about US postsecondary schools
	echo -n "Downloading information about US postsecondary schools ... "
	cd ../schools/
	for ifile in "${!postsecondary_school_locations[@]}"; do
		dcommand="${download_command/-O/}"
		eval "${dcommand} -o ${postsecondary_school_filenames[$ifile]} ${postsecondary_school_locations[$ifile]}"
	done
	echo "DONE"

	echo -n "Extracting the school information ... "
	for zip_file in `ls *.zip`; do
		unzip ${zip_file} > /dev/null
	done
	echo "DONE"

	# Download the list of CCI participants
	echo -n "Downloading the list of CCI participants ... "
	cd ../CCI/
	for file in "${cci_participants[@]}"; do
	    filename=`basename ${file}`
	    #curl -o /opt/WDTSscraper/data/CCI/${filename} ${file}
		eval "${download_command} ${file}"
	done
	echo "DONE"

	# Download the list of SCGSR participants
	echo -n "Downloading the list of SCGSR participants ... "
	cd ../SCGSR/
	for file in "${scgsr_participants[@]}"; do
    	filename=`basename ${file}`
    	eval "${download_command} ${file}"
	done
	echo "DONE"

	# Download the list of SULI participants
	echo -n "Downloading the list of SULI participants ... "
	cd ../SULI/
	for file in "${suli_participants[@]}"; do
	    filename=`basename ${file}`
	    eval "${download_command} ${file}"
	done
	echo "DONE"

	# Download the list of VFP participants
	echo -n "Downloading the list of VFP participants ... "
	cd ../VFP/
	for file in "${vfp_participants[@]}"; do
	    filename=`basename ${file}`
	    eval "${download_command} ${file}"
	done
	echo "DONE"

	cd ../..
fi

echo -e "\nAll files downloaded!"