#!/bin/env python3

"""A magicconfig file used to define a set of options used by the WDTSscraper module.

This specific configuration specifies that only the data for the SCGSR program should be used for the years 2015-2021.
"""

from magiconfig import MagiConfig

config = MagiConfig()
config.files = [
    "data/SCGSR/2015-Sol-1-SCGSR-Award-Public-Announcement.pdf",
    "data/SCGSR/2015-Solicitation-2-SCGSR-Awards---Public-Announcement.pdf",
    "data/SCGSR/2016-Solicitation-1-SCGSR-Awards-Public-Announcement.pdf",
    "data/SCGSR/2016-Solicitation-2-SCGSR-Awards-Management-Public-Annoucement.pdf",
    "data/SCGSR/2017-Solicitation-1-SCGSR-Awards-Public-Announcement.pdf",
    "data/SCGSR/SCGSR-2017-Solicitation-2-Awards---Public-Announcement.pdf",
    "data/SCGSR/2018-Solicitation-1-SCGSR-Awards--Public-Announcement.pdf",
    "data/SCGSR/2018-Solicitation-2-SCGSR-Awards--Public-Announcement.pdf",
    "data/SCGSR/2019-Solicitation-1-SCGSR-Awards-Management-Public-Announcement.pdf",
    "data/SCGSR/2019-Solicitation-2-SCGSR-Awards-Management---Public-Announcement.pdf",
    "data/SCGSR/SCGSR-2020-S2-Awards--public-announcement.pdf",
    "data/SCGSR/SCGSR-2020-Solicitation-1-Awards---Public-Annoucement.pdf",
    "data/SCGSR/SCGSR-2021-S1-Awards--public-announcement-SCGSRwebsite.pdf",
]
config.types = [
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
    "SCGSR",
]
config.years = [
    2015,
    2015,
    2016,
    2016,
    2017,
    2017,
    2018,
    2018,
    2019,
    2019,
    2020,
    2020,
    2021,
]
config.no_lines = False
config.filter_by_topic = False
config.strict_filtering = False
config.debug = False
