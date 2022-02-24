#!/bin/bash

# All From: https://science.osti.gov/wdts/suli
solicitations=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/2020-SULI-participants.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2019.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2018_a.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/SULI-participants-2017.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/2016-SULI-Terms_Participant-Report.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/2015-SULI-Terms_Participant-Report.pdf"
               "https://science.osti.gov/-/media/wdts/suli/pdf/2014-SULI-Terms_Participant-Report.pdf")

for file in "${solicitations[@]}"; do
    filename=`basename ${file}`
    curl -o /opt/WDTSscraper/data/SULI/${filename} ${file}
done
