from magiconfig import MagiConfig

config = MagiConfig()
config.files = [
    "data/SULI/2015-SULI-Terms_Participant-Report.pdf",
    "data/SULI/2016-SULI-Terms_Participant-Report.pdf",
    "data/SULI/SULI-participants-2017.pdf",
    "data/SULI/SULI-participants-2018_a.pdf",
    "data/SULI/SULI-participants-2019.pdf",
    "data/SULI/2020-SULI-participants.pdf",
    "data/SULI/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
]
config.types = [
    "SULI",
    "SULI",
    "SULI",
    "SULI",
    "SULI",
    "SULI",
    "SULI",
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
