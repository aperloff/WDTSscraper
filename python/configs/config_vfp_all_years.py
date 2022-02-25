#!/bin/env python3

"""A magicconfig file used to define a set of options used by the WDTSscraper module.

This specific configuration specifies that only the data for the VFP program should be used for the years 2015-2021.
"""

from magiconfig import MagiConfig

config = MagiConfig()
config.files = [
    "data/VFP/2015-VFP-Faculty-Terms_Participant-Report.pdf",
    "data/VFP/2015-VFP-Student-Terms_Participant-Report.pdf",
    "data/VFP/2016-VFP-Faculty-Terms_Participant-Report.pdf",
    "data/VFP/2016-VFP-Student-Terms_Participant-Report.pdf",
    "data/VFP/VFP-F-participants-2017.pdf",
    "data/VFP/VFP-S-participants-2017.pdf",
    "data/VFP/VFP-F-participants-2018.pdf",
    "data/VFP/VFP-S-participants-2018.pdf",
    "data/VFP/VFP-F-participants-2019.pdf",
    "data/VFP/VFP-S-participants-2019.pdf",
    "data/VFP/2020-VFP-F-participants.pdf",
    "data/VFP/2020-VFP-S-participants.pdf",
    "data/VFP/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
]
config.types = [
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
    "VFP",
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
