#!/bin/bash

# All From: https://science.osti.gov/wdts/scgsr/SCGSR-Awards
solicitations=("https://science.osti.gov/-/media/wdts/scgsr/pdf/SCGSR-2021-S1-Awards--public-announcement-SCGSRwebsite.pdf"
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

for file in "${solicitations[@]}"; do
    filename=`basename ${file}`
    curl -o /opt/WDTSscraper/data/SCGSR/${filename} ${file}
done
