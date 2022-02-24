from magiconfig import MagiConfig

config = MagiConfig()
config.files = [
    "data/SULI/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
    "data/CCI/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
    "data/SCGSR/SCGSR-2021-S1-Awards--public-announcement-SCGSRwebsite.pdf",
    "data/VFP/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
]   
config.types = [
    "SULI",
    "CCI",
    "SCGSR",
    "VFP"
]
config.years = [
    2021,
    2021,
    2021,
    2021,
]
config.no_lines = True
config.filter_by_topic = True
config.strict_filtering = True
