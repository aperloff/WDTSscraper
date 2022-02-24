#!/bin/bash

# All From: https://science.osti.gov/wdts/vfp
solicitations=("https://science.osti.gov/-/media/wdts/pdf/WDTS-SULI-CCI-VFP-Summer-2021.pdf"
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

for file in "${solicitations[@]}"; do
    filename=`basename ${file}`
    curl -o /opt/WDTSscraper/data/VFP/${filename} ${file}
done
