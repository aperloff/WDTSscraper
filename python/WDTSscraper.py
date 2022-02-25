#!/bin/env python3

"""This program DOCSTRING
"""

from argparse import RawTextHelpFormatter
from datetime import date
from enum import Enum
import operator
import os
import sys

import geopandas as gpd
from magiconfig import ArgumentParser, MagiConfigOptions
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import pandas as pd
import pdfplumber

# pylint: disable=C0301
home_institution_replacements = {
    "The Ohio State University Main Campus" : "Ohio State University-Main Campus",
    "State University of New York College at Buffalo" : "University at Buffalo",
    "State University of New York at Binghamton" : "Binghamton University",
    "University at Buffalo-SUNY" : "University at Buffalo",
    "University at Albany, SUNY" : "SUNY at Albany",
    "Saint Joseph's College, New York - Suffolk Campus" : "St. Joseph's College-New York",
    "Universidad del Este" : "Universidad Ana G. Mendez-Carolina Campus",
    "Universidad Del Turabo" : "Universidad del Turabo",
    "University of Tennessee, Knoxville" : "The University of Tennessee-Knoxville",
    "Missouri State University" : "Missouri State University-Springfield",
    "University of Idaho-Idaho Falls" : "University of Idaho",
    "Brigham Young University" : "Brigham Young University-Provo",
    "Wichita State University Campus of Applied Sciences and Technology" : "Wichita State University-Campus of Applied Sciences and Technology",
    "University of New Hampshire" : "University of New Hampshire-Main Campus",
    "Louisiana State University and Agricultural and Mechanical College" : "Louisiana State University and Agricultural & Mechanical College",
    "Georgia Institute of Technology" : "Georgia Institute of Technology-Main Campus",
    "University of Minnesota" : "University of Minnesota-Twin Cities",
    "North Carolina State University" : "North Carolina State University at Raleigh",
    "Indiana University Bloomington" : "Indiana University-Bloomington",
    "University of Oklahoma Norman Campus" : "University of Oklahoma-Norman Campus",
    "Oklahoma State University" : "Oklahoma State University-Main Campus",
    "University of Maryland College Park" : "University of Maryland-College Park",
    "University of Texas at El Paso" : "The University of Texas at El Paso",
    "University of Texas at Arlington" : "The University of Texas at Arlington",
    "Messiah College" : "Messiah University",
    "University of Massachusetts" : "University of Massachusetts-Boston",
    "Penn State University Park" : "Pennsylvania State University-Main Campus",
    "Arizona State University" : "Arizona State University-Downtown Phoenix",
    "Texas A&M University--Kingsville" : "Texas A & M University-Kingsville",
    "Texas A&M University" : "Texas A & M University-College Station",
    "University of Pittsburgh" : "University of Pittsburgh-Pittsburgh Campus",
    "Calvin College" : "Calvin University",
    "City University of New York The City College" : "CUNY City College",
    "Missouri University of Science & Technology" : "Missouri University of Science and Technology",
    "University of Maryland Baltimore County" : "University of Maryland-Baltimore County",
    "The University of Montana - Missoula" : "The University of Montana - Missoula College",
    "Franklin W. Olin College of Engineering" : "Franklin W Olin College of Engineering",
    "Colorado State University" : "Colorado State University-Fort Collins",
    "Saint John's University" : "St. John's University-New York",
    "The University of Utah" : "University of Utah",
    "University of Texas at Austin" : "The University of Texas at Austin",
    "University of Virginia" : "University of Virginia-Main Campus",
    "Tulane University" : "Tulane University of Louisiana",
    "University of Washington" : "University of Washington-Seattle Campus",
    "Cooper Union" : "Cooper Union for the Advancement of Science and Art",
    "Purdue University Main Campus" : "Purdue University-Main Campus",
    "College of William and Mary" : "William & Mary",
    "Herbert H. Lehman College" : "CUNY Lehman College",
    "State University of New York at Stony Brook" : "Stony Brook University",
    "University of Texas--Pan American" : "The University of Texas Rio Grande Valley",
    "Embry-Riddle Aeronautical University" : "Embry-Riddle Aeronautical University-Worldwide",
    "Embry-Riddle Aeronautical University-Prescott Campus" : "Embry-Riddle Aeronautical University-Prescott",
    "Rutgers University - New Brunswick" : "Rutgers University-New Brunswick",
    "Rutgers the State University of New Jersey New Brunswick Campus" : "Rutgers University-New Brunswick",
    "Rutgers University - Newark" : "Rutgers University-Newark",
    "City University of New York Hunter College" : "CUNY Hunter College",
    "Washington University in St. Louis" : "Washington University in St Louis",
    "University of South Carolina-Aiken" : "University of South Carolina Aiken",
    "State University of New York College at Geneseo" : "SUNY College at Geneseo",
    "University of Colorado at Colorado Springs" : "University of Colorado Colorado Springs",
    "Miami University" : "Miami University-Oxford",
    "University of Cincinnati Main Campus" : "University of Cincinnati-Main Campus",
    "University of Tennessee at Chattanooga" : "The University of Tennessee-Chattanooga",
    "University of Texas at Dallas" : "The University of Texas at Dallas",
    "Ohio University Main Campus" : "Ohio University-Main Campus",
    "Inter American University of Puerto Rico San German Campus" : "Inter American University of Puerto Rico-San German",
    "Inter American University of Puerto Rico Aguadilla Campus" : "Inter American University of Puerto Rico-Aguadilla",
    "University of Puerto Rico Rio Piedras Campus" : "University of Puerto Rico-Rio Piedras",
    "University of Puerto Rico - Mayaguez Campus" : "University of Puerto Rico-Mayaguez",
    "University of Puerto Rico Mayaguez Campus" : "University of Puerto Rico-Mayaguez",
    "University of Puerto Rico - Mayaguez" : "University of Puerto Rico-Mayaguez",
    "University of Puerto Rico at Arecibo" : "University of Puerto Rico-Arecibo",
    "University of Puerto Rico at Utuado" : "University of Puerto Rico-Utuado",
    "University of Puerto Rico-Aquadilla" : "University of Puerto Rico-Aguadilla",
    "Milligan College" : "Milligan University",
    "University of New Mexico Main Campus" : "University of New Mexico-Main Campus",
    "State University of New York College of Environmental Science and Forestry" : "SUNY College of Environmental Science and Forestry",
    "State University of New York at Oneonta" : "SUNY Oneonta",
    "State University of New York College at Oneonta" : "SUNY Oneonta",
    "State University of New York at Fredonia" : "SUNY at Fredonia",
    "Penn State Erie, The Behrend College" : "Pennsylvania State University-Penn State Erie-Behrend College",
    "John Jay College" : "CUNY John Jay College of Criminal Justice",
    "College of Du Page" : "College of DuPage",
    "Harper College" : "William Rainey Harper College",
    "La Guardia Community College/City University of New York" : "CUNY LaGuardia Community College",
    "Suffolk County Community College Ammerman Campus" : "Suffolk County Community College",
    "Suffolk County Community College Grant Campus" : "Suffolk County Community College",
    "City University of New York Queensborough Community College" : "CUNY Queensborough Community College",
    "City University of New York Kingsborough Community College" : "CUNY Kingsborough Community College",
    "City University of New York Bronx Community College" : "CUNY Bronx Community College",
    "City University of New York Medger Evers College" : "CUNY Medgar Evers College",
    "Hostos Community College-City University of New York" : "CUNY Hostos Community College",
    "City Colleges of Chicago Harold Washington College" : "City Colleges of Chicago-Harold Washington College",
    "City Colleges of Chicago Wilbur Wright College" : "City Colleges of Chicago-Wilbur Wright College",
    "LIU Post" : "Long Island University",
    "Bethune Cookman University" : "Bethune-Cookman University",
    "University of Houston--Clear Lake" : "University of Houston-Clear Lake",
    "Louisiana State University at Alexandria" : "Louisiana State University-Alexandria",
    "Texas A&M University - Commerce" : "Texas A & M University-Commerce",
    "Southern University and A&M College" : "Southern University and A & M College",
    "Moorhead State University Moorhead" : "M State - Moorhead Campus",
    "University of Illinois at Urbana- Champaign" : "University of Illinois at Urbana-Champaign",
    "Kent State University Kent Campus" : "Kent State University at Kent",
    "Kent State University Main Campus" : "Kent State University at Kent",
    "University of California - Merced" : "University of California-Merced",
    "University of Arkansas Main Campus" : "University of Arkansas",
    "University of Massachusetts Boston" : "University of Massachusetts-Boston",
    "University of Massachusetts Lowell" : "University of Massachusetts-Lowell",
    "University of Kansas Main Campus" : "University of Kansas",
    "University of South Florida" : "University of South Florida-Main Campus",
    "Polytechnic Institute of New York University" : "New York University",
    "Central Methodist University" : "Central Methodist University-College of Liberal Arts and Sciences",
    "Indiana University of Pennsylvania" : "Indiana University of Pennsylvania-Main Campus",
    "York College of Pennsylvania" : "York College Pennsylvania",
    "The University of Memphis" : "University of Memphis",
    "Indiana University-Purdue University Indianapolis" : "Indiana University-Purdue University-Indianapolis",
    "Linfield College" : "Linfield College-McMinnville Campus",
    "Southern Illinois University Carbondale" : "Southern Illinois University-Carbondale",
    "Montana Tech of The University of Montana" : "Montana Tech of the University of Montana",
    "Syracuse University Main Campus" : "Syracuse University",
    "University of West Florida" : "The University of West Florida",
    "Indiana University-Purdue University Fort Wayne" : "Indiana University-Purdue University-Fort Wayne",
    "Paul Smith's College" : "Paul Smiths College of Arts and Science",
    "Concordia University Chicago" : "Concordia University-Chicago",
    "Dixie State College of Utah" : "Dixie State University",
    "City Colleges of Chicago" : "City Colleges of Chicago-District Office",
    "Southern Illinois University Edwardsville" : "Southern Illinois University-Edwardsville",
    "Bowling Green State University" : "Bowling Green State University-Main Campus",
    "University of Saint Thomas" : "University of St Thomas",
    "Georgia Perimeter College" : "Georgia State University-Perimeter College",
    "University of North Carolina at Wilmington" : "University of North Carolina Wilmington",
    "The University of Scranton" : "University of Scranton",
    "Doane College" : "Doane University-Arts & Sciences",
    "University of Massachusetts Dartmouth" : "University of Massachusetts-Dartmouth",
    "University of Houston--Downtown" : "University of Houston-Downtown",
    "Scott Community College" : "Fort Scott Community College",
    "Earlham College and Earlham School of Religion" : "Earlham College",
    "Nazareth College of Rochester" : "Nazareth College",
    "State University of New York, The College at Brockport" : "SUNY College at Brockport",
    "University of Colorado Denver|Anschutz Medical Campus" : "",
    "St. Cloud State University" : "Saint Cloud State University",
    "University of Texas at San Antonio" : "The University of Texas at San Antonio",
    "University of Northwestern - St. Paul" : "University of Northwestern-St Paul",
    "Philadelphia University" : "Jefferson (Philadelphia University + Thomas Jefferson University)",
    "The University of Akron, Main Campus" : "University of Akron Main Campus",
    "Universidad Ana G. Mendez-Gurabo Campus" : "Universidad Ana G. Mendez",
    "University of New Mexico-Los Alamos" : "University of New Mexico-Los Alamos Campus",
    "Furman University" : "Furman",
    "Universidad Metropolitana-Cupey" : "Universidad Metropolitana",
    "Sewanee: The University of the South" : "Sewanee-The University of the South",
    "University of Houston--Victoria" : "University of Houston-Victoria",
    "Johnson State College" : "Northern Vermont University",
    "University of the Sciences in Philadelphia" : "University of the Sciences",
    "Lynchburg College" : "University of Lynchburg",
    "Birmingham-Southern College" : "Birmingham Southern College",
    "Oakland Community College Highland Lakes" : "Oakland Community College",
    "Colorado State University-Pueblo" : "Colorado State University Pueblo",
    "Seattle Central Community College" : "Seattle Central College",
    "City Colleges of Chicago Richard J. Daley College" : "City Colleges of Chicago-Richard J Daley College",
    "El Camino College" : "El Camino Community College District",
    "Yakima Valley Community College" : "Yakima Valley College",
    "The Community College of Baltimore County" : "Community College of Baltimore County",
    "Cuyahoga Community College" : "Cuyahoga Community College District",
    "Suffolk County Community College Eastern Campus" : "Suffolk County Community College",
    "San Jacinto College South" : "San Jacinto College-South Campus",
    "Metropolitan Community College - Maple Woods" : "Metropolitan Community College Area",
    "Des Moines Area Community College, Boone Campus" : "Des Moines Area Community College",
    "Northampton Community College" : "Northampton County Area Community College",
    "City University of New York Herbert H. Lehman College" : "CUNY Lehman College",
}
# pylint: enable=C0301

class ExtendedEnum(Enum):
    """From: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class"""
    @classmethod
    def list_names(cls):
        return list(map(lambda c: c.name, cls))

    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))

class Institution:
    """A class which contains the information about a single laboratory."""
    def __init__(self, name, city, state, latitude, longitude):
        self.name = name
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Institution({self.name})"

class Jobs(ExtendedEnum):
    # pylint: disable=C0103
    Faculty = "Faculty"
    Student = "Student"
    Unknown = "Unknown"

class Laboratory:
    """A class which contains the information about a single laboratory."""
    def __init__(self, name, abbreviation, city, state, latitude, longitude):
        self.name = name
        self.abbreviation = abbreviation
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"Laboratory({self.name} ({self.abbreviation}))"

    def location(self):
        return f"{self.city}, {self.state}"

class Laboratories(ExtendedEnum):
    """
    https://www.findlatitudeandlongitude.com/find-latitude-and-longitude-from-address/
    https://www.latlong.net/
    """

    # pylint: disable=C0103
    AMES = Laboratory("Ames National Laboratory","AMES","Ames","IA",42.02997,-93.648319)
    Ames_National_Laboratory = AMES
    ANL = Laboratory("Argonne National Laboratory","ANL","Argonne","IL",37.037853,-95.821369)
    Argonne_National_Laboratory = ANL
    BNL = Laboratory("Brookhaven National Laboratory","BNL","Upton","NY",40.880610,-72.864810)
    Brookhaven_National_Laboratory = BNL
    DNR = Laboratory("NNSA Naval Reactors Program","DNR","Idaho Falls","ID",43.54446097491455,-112.03437145614816)
    DOE_Naval_Reactors = DNR
    NNSA_Naval_Reactors_Program = DNR
    FNAL = Laboratory("Fermi National Accelerator Laboratory","FNAL","Batavia","IL",41.845584,-88.230627)
    Fermi_National_Accelerator_Laboratory = FNAL
    GA_DIII_D = Laboratory("General Atomics DIII-D Research Program","GA/DIII-D","San Diego","CA",32.893898258647575,-117.23595545378129)
    General_Atomics_DIII_D = GA_DIII_D
    INL = Laboratory("Idaho National Laboratory","INL","Idaho Falls","ID",43.520832,-112.049069)
    Idaho_National_Laboratory = INL
    LBNL = Laboratory("Lawrence Berkeley National Laboratory","LBNL","Berkeley","CA",37.875928,-122.250027)
    Lawrence_Berkeley_National_Laboratory = LBNL
    LLNL = Laboratory("Lawrence Livermore National Laboratory","LLNL","Livermore","CA",37.689684,-121.706508)
    Lawrence_Livermore_National_Laboratory = LLNL
    LANL = Laboratory("Los Alamos National Laboratory","LANL","Los Alamos","NM",35.823204,-106.315255)
    Los_Alamos_National_Laboratory = LANL
    NREL = Laboratory("National Renewable Energy Laboratory","NREL","Golden","CO",39.740555,-105.167442)
    National_Renewable_Energy_Laboratory = NREL
    NETL = Laboratory("National Energy Technology Laboratory","NETL","Pittsburgh","PA",44.623157,-123.120658)
    National_Energy_Technology_Laboratory = NETL
    ORNL = Laboratory("Oak Ridge National Laboratory","ORNL","Oak Ridge","TN",35.930065,-84.3124)
    Oak_Ridge_National_Laboratory = ORNL
    PNNL = Laboratory("Pacific Northwest National Laboratory","PNNL","Richland","WA",48.624371,-122.414436)
    Pacific_Northwest_National_Laboratory = PNNL
    PPPL = Laboratory("Princeton Plasma Physics Laboratory","PPPL","Princeton","NJ",40.35017000292229,-74.60301244421065)
    Princeton_Plasma_Physics_Laboratory = PPPL
    SNL_CA = Laboratory("Sandia National Laboratories","SNL CA","Livermore","CA",37.67632034546966,-121.70583626387636)
    Sandia_National_Laboratories_CA = SNL_CA
    Sandia_National_Laboratory_CA = SNL_CA
    SNL_NM = Laboratory("Sandia National Laboratories","SNL NM","Albuquerque","NM",35.06081338310055,-106.5346557138103)
    Sandia_National_Laboratories_NM = SNL_NM
    Sandia_National_Laboratory_NM = SNL_NM
    SRNL = Laboratory("Savannah River National Laboratory","SRNL","Aiken","SC",33.34290917466783,-81.7378274597186)
    Savannah_River_National_Laboratory = SRNL
    SLAC = Laboratory("SLAC National Accelerator Laboratory","SLAC","Menlo Park","CA",37.420121,-122.205991)
    SLAC_National_Accelerator_Laboratory = SLAC
    TJNAF = Laboratory("Thomas Jefferson National Accelerator Facility","TJNAF","Newport News","VA",37.098362,-76.482427)
    Thomas_Jefferson_National_Accelerator_Facility = TJNAF

    def __repr__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.value.__repr__()}>"

class Person:
    """A class which contains the information about a single person."""

    def __init__(self, program, job, first_name, last_name, home_institution, host_doe_laboratory, topic, year):
        self.program = program
        self.job = job
        self.first_name = first_name
        self.last_name = last_name
        self.home_institution = home_institution
        self.host_doe_laboratory = host_doe_laboratory
        self.topic = topic
        self.year = year

    def __repr__(self):
        return (
            f"Person({self.program} | {self.job} | {self.participant()} | {self.home_institution} | "
            f"{self.host_doe_laboratory.__repr__()} | {self.topic} | {self.year})"
        )

    def participant(self):
        return f"{self.last_name}, {self.first_name}"

def append_institutions(schools, year, inst_name):
    df2 = pd.DataFrame(
        {
            inst_name : [
                "Woods Hole Oceanographic Institution", "Arts et Metiers ParisTech", "University of Canterbury", "McGill University",
                "Trinity College Dublin", "Wilfrid Laurier University", "University of Melbourne", "University of Oxford",
                "Imperial College London", "National Tsing Hua University", "University of Toronto", "Pensacola Christian College",
                "University of Durham", "University of British Columbia",
                "Universidad de Antioquia", "University of Padua"
            ],
            "CITY" : [
                "Falmouth", "Paris", "Christchurch", "Montreal", "Dublin", "Waterloo", "Melbourne", "Oxford", "London", "Hsinchu City",
                "Toronto", "Pensacola", "Durham", "Vancouver", "Antioquia", "Padova PD"
            ],
            "STABBR" if year == 2015 else "STATE" : [
                "MA", "France", "New Zealand", "Canada", "Ireland", "Canada", "Australia", "United Kingdom", "United Kingdom",
                 "Taiwan", "Canada", "FL", "United Kingdom", "Canada", "Colombia", "Italy"
            ],
            "LAT1516" if year == 2015 else "LAT" : [
                41.524781001932716, 48.833508810585855, -43.52243692283857, 45.50543135620449,
                53.34434434753582, 43.474536145835756, -37.798583273349905, 51.75540084373608, 51.49896243904694,
                24.796345696985465, 43.661591621428244, 30.473591759462174, 54.765146814889256, 49.260822236130316,
                6.2689002766401485, 45.40693922363649
            ],
            "LON1516" if year == 2015 else "LON" : [
                -70.6711607, 2.358395261383819, 172.5800791301893, -73.57646445446471,
                -6.254485769308092, -80.5273405693174, 144.96136023807165, -1.2540234772696208, -0.174830586222553,
                120.99670208429329, -79.39612346136519, -87.23406222329352, -1.5780956131069162, -123.24589724211424,
                -75.56872258272178, 11.877499842431922
            ],
        },
    )
    schools = pd.concat([schools, df2], ignore_index = True, axis = 0)
    return schools

def filter_people_by_topic(people, strict):
    return [person for person in people if (not strict and not person.topic) or any(t in person.topic for t in ["HEP", "High Energy Physics"])]

def handle_known_issues_parsing_input(lines, year, debug = False):
    if debug:
        print("Handling known parsing issues ...")
    for iline, line in enumerate(lines):
        if debug:
            print(line)
        tmp = []
        if any("Thomas Jefferson National" in item for item in line):
            tmp = line[0:3]
            tmp += line[3].split("TJNA")
            tmp[3] += "TJNAF)"

        # 2021
        if year == 2021 and "Ouango, Boinzemwende Jarmila Roxa" in line[1]:
            tmp = line[0:1]
            tmp += line[1].split("Roxa")
            tmp[1] += "Roxane"
            tmp += line[2:]

        # 2020
        if year == 2020 and len(line) >=2 and "\"" in line[1]:
            tmp = line[0:1]
            tmp.append(line[1][:line[1].rfind("\"") + 1])
            tmp.append(line[1][line[1].rfind("\"") + 1:])
            tmp += line[2:]
        elif year == 2020 and "Vazquez Olivas" in line[0]:
            tmp = [" ".join(line[0].split()[0:2])] + [line[0].split()[2]] + line[1:]
        elif year == 2020 and "Teutu Talla Serges Love" in line[0]:
            tmp = [" ".join(line[0].split()[0:2])] + [" ".join(line[0].split()[2:4])] + [" ".join(line[0].split()[4:])] + [line[1]]
        elif year == 2020 and (len(line[0].split()) > 1 or len(line[1].split()) > 1):
            for line_part in line:
                tmp += line_part.split()
            if tmp[0] == "De":
                tmp = [" ".join(tmp[0:2])] + tmp[2:]
            tmp = tmp[0:2] + [" ".join(tmp[2:-1] if tmp[-2] != "SNL" else tmp[2:-2])] + ([tmp[-1]] if tmp[-2] != "SNL" else tmp[-2:])
        elif year == 2020 and len(line) == 3 and any(l in line[2] for l in Laboratories.list_names()):
            inst_lab = line[2].split()
            tmp = line[0:2] + [" ".join(inst_lab[0:-1] if inst_lab[-2] != "SNL" else inst_lab[0:-2])] + \
                  ([inst_lab[-1]] if inst_lab[-2] != "SNL" else inst_lab[-2:])

        if len(tmp) > 0:
            if debug:
                print(tmp)
            lines[iline] = tmp

    return lines

def get_institution(schools, home_institution, year, debug = False):
    if debug:
        print(f"Getting the home institution details for {home_institution} ... ", end="")

    inst_name = "INSTNM" if year < 2017 else "NAME"

    # fix a known parsing error (probably a unicode error)
    if "‐" in home_institution:
        home_institution = home_institution.replace("‐", "-")

    # append specific institutions to the existing GeoDataFrame
    schools = append_institutions(schools, year, inst_name)

    # start by trying the original value
    institution = schools.loc[schools[inst_name].isin([home_institution])]

    # replace home_institution with known good values
    if institution.size == 0 and home_institution in home_institution_replacements:
        home_institution = home_institution_replacements[home_institution]
        institution = schools.loc[schools[inst_name].isin([home_institution])]

    # if the institution is still not found, try some more replacements
    if institution.size == 0:
        if "/City University of New York" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["CUNY " + home_institution.replace("/City University of New York", "")])]
        elif "-City University of New York" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["CUNY " + home_institution.replace("-City University of New York", "")])]
        elif "City University of New York" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("City University of New York", "CUNY")])]
        elif "State University of New York" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("State University of New York", "SUNY")])]
        elif "Binghamton University" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["SUNY at Binghamton"])]
        elif "St. Joseph's College-New York" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Saint Joseph's College-New York"])]
        elif "Medical Sciences Campus" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" Medical Sciences Campus", "-Medical Sciences")])]
        elif "Missoula" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["The University of Montana"])]
        elif "Montana Tech of the University of Montana" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Montana Technological University"])]
        elif "Southern Polytechnic State University" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Kennesaw State University"])]
        elif "Long Island University" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["LIU Post"])]
        elif " De " in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" De ", " de ")])]
        elif "St. John Fisher College" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("St. ", "Saint ")])]
        elif "St. " in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("St. ", "St ")])]
        elif "Turabo" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Universidad Ana G. Mendez"])]
        elif "Gurabo" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Universidad Ana G. Mendez"])]
        elif "Ana G. Mendez" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" G. ", " G ")])]
        elif "Paducah Extended Campus" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["University of Kentucky"])]
        elif "California Maritime Academy" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["The " + home_institution])]
        elif "CSU Maritime Academy" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("CSU", "California State University")])]
        elif "Cayey" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" at ", "-")])]
        elif "Texas A & M University-San Antonio" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("A & M", "A&M")])]
        elif "Sewanee:" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["The University of the South"])]
        elif "Quinnipiac College" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("College", "University")])]
        elif "Edinboro University" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution + " of Pennsylvania"])]
        elif "Penn State Berks" in home_institution:
            institution = schools.loc[schools[inst_name].isin(["Pennsylvania State University-" + home_institution])]
        elif "A&M" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("A&M", "A & M").replace(" - ", "-")])]
        elif "Agricultural and Mechanical" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("Agricultural and Mechanical", "A & M")])]
        elif "Agricultural and Technical" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace("Agricultural and Technical", "A & T")])]
        elif "Main Campus" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" Main Campus", "-Main Campus")])]
        elif " and" in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" and", " &")])]
        elif " - " in home_institution:
            institution = schools.loc[schools[inst_name].isin([home_institution.replace(" - ", "-")])]

    if institution.size == 0:
        if debug:
            print(f"\n\tWARNING::{home_institution} not found (year = {year}).")
        institution = None
    elif institution is not None and institution.size != 0:
        if debug:
            print("DONE")

        institution = Institution(
            name = institution.iloc[0][inst_name],
            city = institution.iloc[0]['CITY'],
            state = institution.iloc[0]['STABBR'] if year == 2015 else institution.iloc[0]['STATE'],
            latitude = institution.iloc[0]['LAT1516'] if year == 2015 else institution.iloc[0]['LAT'],
            longitude = institution.iloc[0]['LON1516'] if year == 2015 else institution.iloc[0]['LON'],
        )
        return institution
    else:
        return None

def load_schools(year):
    # load the database for the home institutions
    schools = None
    if year == 2021:
        schools = gpd.read_file("data/schools/EDGE_GEOCODE_POSTSECONDARYSCH_CURRENT.shp")
    else:
        schools = gpd.read_file(f"data/schools/Postsecondary_School_Locations_{year}-{year - 1999}.shp")
    return schools

def hanging_line(point1, point2):
    """
    https://stackoverflow.com/questions/30008322/draw-a-curve-connecting-two-points-instead-of-a-straight-line
    """

    #pylint: disable=C0103
    a = (point2[1] - point1[1])/(np.cosh(point2[0]) - np.cosh(point1[0]))
    b = point1[1] - a*np.cosh(point1[0])
    x = np.linspace(point1[0], point2[0], 100)
    y = a*np.cosh(x) + b

    return (x,y)

def plot_map(debug = False, formats = None, lines = True, output_path = "./", person_data = None, show = False, states = None, us_map = True):
    usa = gpd.read_file("/opt/WDTSscraper/data/us_map/cb_2020_us_state_500k.shp")
    #print(usa.columns)
    #usa['NAME']
    #usa.loc[2, 'NAME']
    #usa.loc[2, ['NAME','geometry']]
    #map = usa.plot()
    #usa[usa.NAME == "California"].plot()

    # matplotlib colors - https://matplotlib.org/stable/gallery/color/named_colors.html
    # Data - https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
    # Basic plotting - https://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states
    # Basic plotting - https://medium.com/@erikgreenj/mapping-us-states-with-geopandas-made-simple-d7b6e66fa20d
    # More advanced plotting - https://jcutrer.com/python/learn-geopandas-plotting-usmaps
    # Advanced plotting - https://geopandas.org/en/stable/gallery/plotting_basemap_background.html
    # Move AK and HI - https://stackoverflow.com/questions/69278742/rearranging-polygons-in-geopandas-for-matplotlib-plotting
    # Tight left and right margins - https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot

    # set state code as index, exclude states that we will never display
    usa = usa.set_index('STUSPS').drop(index=['VI', 'MP', 'GU', 'AS'])
    if debug:
        print(usa[['NAME','geometry']])

    # create an axis with the insets − this defines the inset sizes
    fig, continental_ax = plt.subplots(figsize=(20, 10))
    alaska_ax = continental_ax.inset_axes([.055, -.0525, .225, .315]) # [x0, y0, width, height]
    hawaii_ax = continental_ax.inset_axes([.279, .01, .15, .19]) # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.inset_axes.html
    puerto_rico_ax = continental_ax.inset_axes([.8, -.01, .15, .19])

    # Set bounds to fit desired areas in each plot
    continental_ax.set_xlim(-130, -64)
    continental_ax.set_ylim(22, 53)

    alaska_ax.set_ylim(51, 72)
    alaska_ax.set_xlim(-180, -127)

    hawaii_ax.set_ylim(18.8, 22.5)
    hawaii_ax.set_xlim(-160, -154.6)

    puerto_rico_ax.set_ylim(17.5, 19)
    puerto_rico_ax.set_xlim(-68.25, -65)

    # Plot the data per area - requires passing the same choropleth parameters to each call
    # because different data is used in each call, so automatically setting bounds won’t work
    usa.drop(index=['HI', 'AK', 'PR']).plot(ax = continental_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['AK']].plot(ax = alaska_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['HI']].plot(ax = hawaii_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')
    usa.loc[['PR']].plot(ax = puerto_rico_ax, color = "Grey", linewidth = 0.25, edgecolor = 'k')

    if states is not None:
        selection = usa[usa.index.isin(states)]
        selection.plot(ax = continental_ax, cmap = 'OrRd', figsize = (25, 14)) # color = "DarkGray"

    # start keeping track of the legend items
    legend_artists = []
    legend_artists.append(
        mlines.Line2D(
            [],
            [],
            color='red',
            marker = "*",
            markersize=12,
            linestyle = None,
            linewidth = 0,
            label='DOE Laboratory'
        )
    )

    # get the university markers
    if lines:
        inst_df = pd.DataFrame(
            {
                'Inst': [person.home_institution.name for person in person_data if person.home_institution is not None],
                'Latitude': [person.home_institution.latitude for person in person_data if person.home_institution is not None],
                'Longitude': [person.home_institution.longitude for person in person_data if person.home_institution is not None],
            }
        )
        inst_gdf = gpd.GeoDataFrame(
            inst_df, geometry=gpd.points_from_xy(inst_df.Longitude, inst_df.Latitude)
        )
        if debug:
            print(inst_gdf.head())
        inst_gdf.plot(ax = continental_ax, color = 'blue')
        inst_gdf.plot(ax = alaska_ax, color = 'blue')
        inst_gdf.plot(ax = hawaii_ax, color = 'blue')
        inst_gdf.plot(ax = puerto_rico_ax, color = 'blue')

        legend_artists.append(
            mlines.Line2D(
                [],
                [],
                color='blue',
                marker = ".",
                markersize=12,
                linestyle = None,
                linewidth = 0,
                label='Home Institution'
            )
        )
    else:
        # define a set of markers
        markers = ["o", "v", "^", "s", "p", "P", "D", "d", "X","*"]
        colors = [
            "lightskyblue", "deepskyblue", "cornflowerblue", "dodgerblue", "royalblue",
            "blue", "mediumblue", "darkblue", "navy", "midnightblue",
        ]

        # get the set of programs from list of people
        programs = set()
        for person in person_data:
            programs.add(person.program)

        if debug:
            print(programs)

        # loop over the programs and draw each on separately
        for iprogram, program in enumerate(sorted(programs)):
            inst_df = pd.DataFrame(
                {
                    'Inst': [person.home_institution.name for person in person_data \
                             if person.home_institution is not None and person.program == program],
                    'Latitude': [person.home_institution.latitude for person in person_data \
                                 if person.home_institution is not None and person.program == program],
                    'Longitude': [person.home_institution.longitude for person in person_data \
                                  if person.home_institution is not None and person.program == program],
                }
            )
            inst_gdf = gpd.GeoDataFrame(
                inst_df, geometry=gpd.points_from_xy(inst_df.Longitude, inst_df.Latitude)
            )
            if debug:
                print(inst_gdf.head())
            inst_gdf.plot(ax = continental_ax, color = colors[iprogram], marker = markers[iprogram])
            inst_gdf.plot(ax = alaska_ax, color = colors[iprogram], marker = markers[iprogram])
            inst_gdf.plot(ax = hawaii_ax, color = colors[iprogram], marker = markers[iprogram])
            inst_gdf.plot(ax = puerto_rico_ax, color = colors[iprogram], marker = markers[iprogram])

            legend_artists.append(
                mlines.Line2D(
                    [],
                    [],
                    color = colors[iprogram],
                    marker = markers[iprogram],
                    markersize=12,
                    linestyle = None,
                    linewidth = 0,
                    label = f'Home Institution ({program})'
                )
            )

    # get the laboratory markers
    lab_df = pd.DataFrame(
        {
            'Lab': [l.abbreviation for l in Laboratories.list_values()],
            'Latitude': [l.latitude for l in Laboratories.list_values()],
            'Longitude': [l.longitude for l in Laboratories.list_values()],
        }
    )
    lab_gdf = gpd.GeoDataFrame(
        lab_df, geometry=gpd.points_from_xy(lab_df.Longitude, lab_df.Latitude)
    )
    if debug:
        print(lab_gdf.head())
    lab_gdf.plot(ax = continental_ax, color = 'red', marker = '*', markersize = 60)
    lab_gdf.plot(ax = alaska_ax, color = 'red', marker = '*', markersize = 60)
    lab_gdf.plot(ax = hawaii_ax, color = 'red', marker = '*', markersize = 60)
    lab_gdf.plot(ax = puerto_rico_ax, color = 'red', marker = '*', markersize = 60)

    #  draw the lines between labs and institutions
    if lines:
        legend_artists.append(mlines.Line2D([], [], color='orange', linestyle = "-", label='Faculty'))
        legend_artists.append(mlines.Line2D([], [], color='yellow', linestyle = "--", label='Student'))
        for person in person_data:
            if person.home_institution is None:
                continue
            start_location = [person.home_institution.longitude, person.home_institution.latitude]
            end_location = [person.host_doe_laboratory.value.longitude, person.host_doe_laboratory.value.latitude]
            x, y = hanging_line(start_location, end_location)
            continental_ax.plot(
                x,
                y,
                linewidth = 1 if person.job == Jobs.Student else 2,
                linestyle = "--" if person.job == Jobs.Student else "-",
                color = "yellow" if person.job == Jobs.Student else "orange"
            )
            alaska_ax.plot(
                x,
                y,
                linewidth = 1 if person.job == Jobs.Student else 2,
                linestyle = "--" if person.job == Jobs.Student else "-",
                color = "yellow" if person.job == Jobs.Student else "orange"
            )
            hawaii_ax.plot(
                x,
                y,
                linewidth = 1 if person.job == Jobs.Student else 2,
                linestyle = "--" if person.job == Jobs.Student else "-",
                color = "yellow" if person.job == Jobs.Student else "orange"
            )
            puerto_rico_ax.plot(
                x,
                y,
                linewidth = 1 if person.job == Jobs.Student else 2,
                linestyle = "--" if person.job == Jobs.Student else "-",
                color = "yellow" if person.job == Jobs.Student else "orange"
            )

    # Add a legend
    continental_ax.legend(handles=legend_artists, prop={'size': 16}, facecolor='Grey', loc='upper right')

    # remove ticks
    for ax in [continental_ax, alaska_ax, hawaii_ax, puerto_rico_ax]:
        ax.set_yticks([])
        ax.set_xticks([])

    # remove the axes altogether
    #plt.axis('off')

    # Reduce the left and right margins
    fig.tight_layout()

    # Save the figure
    if formats is not None:
        for fmt in formats:
            output_filename = f"{output_path}/{date.today().strftime('%Y_%m_%d')}_map"
            i = 0
            while os.path.exists(f"{output_filename}_v{i}.{fmt}"):
                i += 1
            output_filename = f"{output_filename}_v{i}.{fmt}"
            plt.savefig(output_filename, bbox_inches='tight')

    if show:
        plt.show()

def process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic(filename, year, debug = False, program_filter = None, sort = True):
    # declare the return object
    people = []

    # load the database for the home institutions
    schools = load_schools(year)

    # load the pdf of names
    pdf = pdfplumber.open(filename)
    for ipage, page in enumerate(pdf.pages):
        split_lines = page.extract_text(layout = False, x_tolerance = 1).split('\n')
        split_lines_no_blanks = [x.split(' ') for x in split_lines]
        if ipage == 0:
            split_lines_no_blanks = split_lines_no_blanks[3:]
        split_lines_no_blanks = [[item.replace("\xa0", " ").strip() for item in line] for line in split_lines_no_blanks]
        good_lines = handle_known_issues_parsing_input(split_lines_no_blanks, year)
        good_vfp_lines = [line for line in good_lines if any(filter in line[0] for filter in program_filter)] \
                         if program_filter is not None else good_lines
        if len(good_vfp_lines) == 0:
            continue
        people += [Person(program = line[0].split()[0] if " " in line[0] else line[0],
                          job = Jobs[line[0].split()[1] if " " in line[0] else "Student" \
                                     if any(i in line[0] for i in ["SULI", "CCI"]) else "Unknown"],
                          first_name = line[1].split(",")[1],
                          last_name = line[1].split(",")[0],
                          home_institution = get_institution(schools, line[2], year, debug = debug),
                          host_doe_laboratory = Laboratories["GA_DIII_D"] if "General Atomics" in line[3] \
                                                else Laboratories[line[3][line[3].find("(") + 1 : line[3].rfind(")")].replace(" ", "_")],
                          topic = line[4],
                          year = year) if len(line) == 5 else print("ERROR::" + str(line)) for line in good_vfp_lines]

    if sort:
        people.sort(key = operator.attrgetter("job.name"))

    if debug:
        print(people)
    return people

def process_file_table_no_lines_term_lastname_firstname_institution_laboratory(filename, year, debug = False, program_filter = None, sort = True):
    # declare the return object
    people = []

    # load the database for the home institutions
    schools = load_schools(year)

    # load the pdf of names
    pdf = pdfplumber.open(filename)
    for ipage, page in enumerate(pdf.pages):
        lines = [l.split("  ") for l in page.extract_text(layout=True, keep_blank_chars=True, x_tolerance=1).split("\n")]
        lines = [[l for l in line if l] for line in lines]

        # Removes blanks
        lines = [line for line in lines if len(line) > 0]

        # Set the program and job values and then remove the page header and the page numbers
        if ipage == 0:
            program = lines[0][0]
            program = program[program.find("(") + 1 : program.rfind(")")]
            job = Jobs["Student" if "Participants" in lines[0][0] else lines[0][0].split()[-1].capitalize()]
        lines = [line for line in lines if len(line) > 1]

        # Remove the column headers (if they exist)
        if "Term" in lines[0][0]:
            lines = lines[1:]

        for line in lines:
            # Handle case when Institution and Host Lab columns are merged
            #if len(line) == 4 and any(l in line[-1] for l in Laboratories.list_names()):
            #    line = line[:-1] + [" ".join(line[-1].split()[:-1])] + [line[-1].split()[-1]]

            # What to do if the number of columns still isn't right
            if len(line) != 5:
                print("ERROR::" + str(line))
                continue

            # Create the Person object and append it to the list
            people.append(
                Person(
                    program = program,
                    job = job,
                    first_name = line[2].lstrip().strip(),
                    last_name = line[1].lstrip().strip(),
                    home_institution = get_institution(schools, line[3].lstrip().strip(), year, debug = debug),
                    host_doe_laboratory = Laboratories[line[4].lstrip().strip().replace(" / ", "_").replace(" ", "_").replace("-", "_")],
                    topic = "",
                    year = year,
                )
            )

    if sort:
        people.sort(key = operator.attrgetter("job.name"))

    if debug:
        print(people)
    return people

def process_file_table_with_lines_name_institution_laboratory_term(filename, year, debug = False, program_filter = None, sort = True):
    # declare the return object
    people = []

    # load the database for the home institutions
    schools = load_schools(year)

    # load the pdf of names
    pdf = pdfplumber.open(filename)
    program = ""
    job = ""
    for ipage, page in enumerate(pdf.pages):
        table = page.extract_table()
        if table is None:
            continue

        if ipage == 0:
            program = page.extract_text().split("\n")[0]
            program = program[program.find("(") + 1 : program.rfind(")")]
            job = Jobs["Student" if table[0][0].split()[1].capitalize() == "Participant" else table[0][0].split()[1].capitalize()]
            table = table[1:]
        if ipage > 0 and "PARTICIPANT" in table[0][0]:
            table = table[1:]

        for row in table:
            # Check for blank rows
            if all(not r for r in row):
                continue

            # Find the laboratory information
            lab = ""
            if "(" in row[2]:
                lab = row[2][row[2].find("(") + 1:row[2].rfind(")")]
            else:
                lab = row[2].replace(" ", "_").replace("\n", "")
            if any(l in lab for l in ["SNL", "Sandia"]):
                lab += "_CA" if any(w in row[1] for w in ["California","Mills"]) else "_NM"
            if any(n in lab for n in ["General Atomics", "General_Atomics","General\xa0Atomics"]):
                lab = "General_Atomics_DIII_D"
            if lab == "TJNA": # Needed because sometimes the lab name gets cut off
                lab = "TJNAF"
            lab = lab.replace("\xa0","_")

            # Get the name and institution of the person
            last_name = row[0].split()[-1]
            first_name = " ".join(row[0].split()[:-1])
            home_institution = " ".join(row[1].split())
            institution = get_institution(schools, home_institution, year, debug = debug)

            # Create the Person object and append it to the list
            people.append(
                Person(
                    program = program,
                    job = job,
                    first_name = first_name,
                    last_name = last_name,
                    home_institution = institution,
                    host_doe_laboratory = Laboratories[lab],
                    topic = "",
                    year = year,
                )
            )

    if sort:
        people.sort(key = operator.attrgetter("job.name"))

    if debug:
        print(people)
    return people

def process_file_table_with_lines_name_institution_laboratory_area(filename, year, debug = False, program_filter = None, sort = True):
    # declare the return object
    people = []

    # load the database for the home institutions
    schools = load_schools(year)

    # load the pdf of names
    pdf = pdfplumber.open(filename)
    program = ""
    job = ""
    for ipage, page in enumerate(pdf.pages):
        table = page.extract_table()
        if ipage == 0:
            program = page.extract_text().split("\n")[0]
            program = program[program.find("(") + 1 : program.rfind(")")]
            job = Jobs["Student" if "Student" in page.extract_text().split("\n")[0] else "Faculty"]
            table = table[1:]
        for row in table:
            lab = ""
            if "(" in row[2] and ")" in row[2]:
                lab = row[2][row[2].find("(") + 1:row[2].rfind(")")]
            else:
                lab = row[2][ : row[2].find("(") - 1].replace(" ", "_").replace("\xa0","_")
            if "SNL" in lab or "Sandia" in lab:
                lab += "_CA" if any(w in row[1] for w in ["California","Mills"]) else "_NM"
            if any(n in lab for n in ["General Atomics", "General_Atomics"]):
                lab = "General_Atomics_DIII_D"
            last_name = row[0].split()[-1]
            first_name = " ".join(row[0].split()[:-1])
            home_institution = " ".join(row[1].split())
            institution = get_institution(schools, home_institution, year, debug = debug)
            people.append(
                Person(
                    program = program,
                    job = job,
                    first_name = first_name,
                    last_name = last_name,
                    home_institution = institution,
                    host_doe_laboratory = Laboratories[lab],
                    topic = row[3].replace("\n", "").strip(),
                    year = year,
                )
            )

    if sort:
        people.sort(key = operator.attrgetter("job.name"))

    if debug:
        print(people)
    return people

def WDTSscraper(debug = False,
                files = None,
                filter_by_topic = False,
                formats = None,
                interactive = False,
                no_draw = False,
                no_lines = False,
                output_path = "./",
                strict_filtering = False,
                types = None,
                years = None):

    if files is None:
        raise ValueError("You must specify at least one file to process.")

    if any(len(lst) != len(files) for lst in [types, years]):
        raise ValueError(f"The number of files ({len(files)}), types ({len(types)}), and years ({len(years)}) must be the same.")

    process_file_map = {
      ('VFP', 2021): process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic,
      ('VFP', 2020): process_file_table_no_lines_term_lastname_firstname_institution_laboratory,
      ('VFP', 2019): process_file_table_with_lines_name_institution_laboratory_term,
      ('VFP', 2018): process_file_table_with_lines_name_institution_laboratory_term,
      ('VFP', 2017): process_file_table_with_lines_name_institution_laboratory_term,
      ('VFP', 2016): process_file_table_with_lines_name_institution_laboratory_term,
      ('VFP', 2015): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2021): process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic,
      ('SULI', 2020): process_file_table_no_lines_term_lastname_firstname_institution_laboratory,
      ('SULI', 2019): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2018): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2017): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2016): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2015): process_file_table_with_lines_name_institution_laboratory_term,
      ('SULI', 2014): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2021): process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic,
      ('CCI', 2020): process_file_table_no_lines_term_lastname_firstname_institution_laboratory,
      ('CCI', 2019): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2018): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2017): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2016): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2015): process_file_table_with_lines_name_institution_laboratory_term,
      ('CCI', 2014): process_file_table_with_lines_name_institution_laboratory_term,
      ('SCGSR', 2021): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2020): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2019): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2018): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2017): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2016): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2015): process_file_table_with_lines_name_institution_laboratory_area,
      ('SCGSR', 2014): process_file_table_with_lines_name_institution_laboratory_area,
    }

    people = []
    for ifile, file in enumerate(files):
        if years[ifile] <= 2014:
            raise RuntimeError("Unfortunately we are unable to get university/institution locations for any year prior to 2015.")
        if (types[ifile], years[ifile]) not in process_file_map:
            raise RuntimeError(f"We don't know how to process {types[ifile]} files for the year {years[ifile]}.")

        print(f"Processing the file {file} (year = {years[ifile]}, program = {types[ifile]}) ... ")
        people += process_file_map[(types[ifile], years[ifile])](file, years[ifile], debug = debug, program_filter = [types[ifile]])

    if filter_by_topic:
        people = filter_people_by_topic(people, strict_filtering)

    if not no_draw:
        plot_map(
            debug = debug,
            formats = formats,
            lines = not no_lines,
            output_path = output_path,
            person_data = people,
            show = interactive,
            states = None,
            us_map = True
        )

if __name__ == "__main__":
    parser = ArgumentParser(config_options=MagiConfigOptions(),
                            formatter_class=RawTextHelpFormatter,
                            description="Scrape WDTS produced PDF files for specific information.",
                            epilog = """examples:
    all options using the command line:
        `python3 WDTSscraper.py -f data/WDTS-SULI-CCI-VFP-Summer-2021.pdf -t VFP -y 2021`

    using a magiconfig file:
        `python3 python/WDTSscraper.py -C python/configs/config_all-programs_2021.py`"""
    )
    parser.add_argument("-d", "--debug", action = "store_true",
                        help="Shows some extra information in order to debug this program (default=%(default)s)")
    parser.add_argument("-f", "--files", nargs = "+",
                        help = "The absolute paths to the files to scrape (default=%(default)s)")
    parser.add_argument("-F", "--formats", nargs = "+", default = ["png"], choices = ["png", "pdf", "ps", "eps", "svg"],
                        help = "List of formats with which to save the resulting map (default=%(default)s)")
    parser.add_argument("-i", "--interactive", action = "store_true",
                        help = "Show the plot during program execution (default=%(default)s)")
    parser.add_argument("-n", "--no-lines", action = "store_true",
                        help = "Do not plot the lines connecting the home institutions and the national laboratories (default=%(default)s)")
    parser.add_argument("-N", "--no-draw", action = "store_true",
                        help = "Do not create or save the resulting map (default=%(default)s)")
    parser.add_argument("-O", "--output-path", default = os.getcwd(),
                        help = "Directory in which to save the resulting maps (default=%(default)s)")
    parser.add_argument("-S", "--strict-filtering", action = "store_true",
                        help = "More tightly filter out participants by removing those whose topic is unknown (default=%(default)s)")
    parser.add_argument("-t", "--types", choices = ["VFP", "SULI", "CCI", "SCGSR"], nargs = "+",
                        help = "A list of the types of files being processed (default=%(default)s)")
    parser.add_argument("-T", "--filter-by-topic", action = "store_true",
                        help = "Filter the participants by topic if the topic is available (default=%(default)s)")
    parser.add_argument("-y", "--years", nargs = "+", type = int,
                        help = "A list of years to help determine how to process each file (default=%(default)s)")
    args = parser.parse_args()

    if args.debug:
        print('Number of arguments:', len(sys.argv), 'arguments.')
        print('Argument List:', str(sys.argv))
        print("Argument", args)

    WDTSscraper(**vars(args))
