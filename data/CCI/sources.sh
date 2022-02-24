#!/bin/bash

# All From: https://science.osti.gov/wdts/CCI
solicitations=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/2020-CCI-participants.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2019.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2018.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/CCI-participants-2017.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/2016-CCI-Terms_Participant-Report.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/2015-CCI-Terms_Participant-Report.pdf"
               "https://science.osti.gov/-/media/wdts/cci/pdf/2014-CCI-Terms_Participant-Report.pdf")

for file in "${solicitations[@]}"; do
    filename=`basename ${file}`
    curl -o /opt/WDTSscraper/data/CCI/${filename} ${file}
done
