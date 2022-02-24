from magiconfig import MagiConfig

config = MagiConfig()
config.files = [
    "data/CCI/2015-CCI-Terms_Participant-Report.pdf",
    "data/CCI/2016-CCI-Terms_Participant-Report.pdf",
    "data/CCI/CCI-participants-2017.pdf",
    "data/CCI/CCI-participants-2018.pdf",
    "data/CCI/CCI-participants-2019.pdf",
    "data/CCI/2020-CCI-participants.pdf",
    "data/CCI/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
]
config.types = [
    "CCI",
    "CCI",
    "CCI",
    "CCI",
    "CCI",
    "CCI",
    "CCI",
]
config.years = [
    2015,
    2016,
    2017,
    2018,
    2019,
    2020,
    2021,
]
config.no_lines = False
config.filter_by_topic = False
config.strict_filtering = False
config.debug = False
