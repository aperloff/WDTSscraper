#!/bin/env python3

"""institution

This module contains functions and classes which are involved in obtaining and storing information
about a person's home institution, usually a college or university.

Constants
---------
home_institution_replacements : dict
    A dict of {str : str} for storing previously encountered institution names and the corresponding names
    in the US Department of Education database

Classes
----------
Institution
    Stores information about a specific institution

Functions
---------
append_institutions
    Add some extra institutions to the database of postsecondary schools
get_institution
    Find the correct postsecondary school in the database, store the relevant information in an Institution
    object, and return that object
load_schools
    Load the correct database of postsecondary school information
"""

import geopandas as gpd
import pandas as pd

# pylint: disable=C0301
home_institution_replacements = {
    "The Ohio State University Main Campus" : "Ohio State University-Main Campus",
    "State University of New York College at Buffalo" : "University at Buffalo",
    "State University of New York at Binghamton" : "Binghamton University",
    "University at Buffalo-SUNY" : "University at Buffalo",
    "University at Albany, SUNY" : "SUNY at Albany",
    "New York City College of Technology/City University of New York" : "CUNY New York City College of Technology",
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
    "City Colleges of Chicago Harry S. Truman College" : "City Colleges of Chicago-Harry S Truman College",
    "LIU Post" : "Long Island University",
    "Long Island University" : "LIU Post",
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
    "Montana Tech of the University of Montana" : "Montana Technological University",
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
    "University of Colorado Denver|Anschutz Medical Campus" : "University of Colorado Denver/Anschutz Medical Campus",
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
    "Southern Polytechnic State University" : "Kennesaw State University",
    "California Maritime Academy" : "The California Maritime Academy",
    "CSU Maritime Academy" : "California State University Maritime Academy",
    "Texas A & M University-San Antonio" : "Texas A&M University-San Antonio",
    "Franklin & Marshall College" : "Franklin and Marshall College",
    "Northwestern State University" : "Northwestern State University of Louisiana",
    "University of Wisconsin Colleges" : "University of Wisconsin Colleges Flex",
}

home_institution_secondary_replacements = {
    "/City University of New York" : ["CUNY", "/City University of New York", ""],
    "-City University of New York" : ["CUNY ", "-City University of New York", ""],
    "City University of New York" : ["City University of New York", "CUNY"],
    "State University of New York" : ["State University of New York", "SUNY"],
    "Binghamton University" : ["SUNY at Binghamton"],
    "St. Joseph's College-New York" : ["Saint Joseph's College-New York"],
    "Montana Tech of The University of Montana" : ["Montana Technological University"],
    "Montana Tech of the University of Montana" : ["Montana Technological University"],
    "Medical Sciences Campus" : [" Medical Sciences Campus", "-Medical Sciences"],
    "Missoula" : ["The University of Montana"],
    " De " : [" De ", " de "],
    "St. John Fisher College" : ["St. ", "Saint "],
    "St. " : ["St. ", "St "],
    "Turabo" : ["Universidad Ana G. Mendez"],
    "Gurabo" : ["Universidad Ana G. Mendez"],
    "Ana G. Mendez" : [" G. ", " G "],
    "Paducah Extended Campus" : ["University of Kentucky"],
    "Cayey" : [" at ", "-"],
    "Sewanee:" : ["The University of the South"],
    "Sewanee-" : ["The University of the South"],
    "Quinnipiac College" : ["Quinnipiac University"],
    "Edinboro University" : ["Edinboro University of Pennsylvania"],
    "Penn State Berks" : ["Pennsylvania State University-Penn State Berks"],
    "A&M" : ["A&M", "A & M", " - ", "-"],
    "Agricultural and Mechanical" : ["Agricultural and Mechanical", "A & M"],
    "Agricultural and Technical" : ["Agricultural and Technical", "A & T"],
    "Main Campus" : [" Main Campus", "-Main Campus"],
    " and" : [" and", " &"],
    " - " : [" - ", "-"],
}
# pylint: enable=C0301

class Institution:
    """A class which contains the information about a single institution.

    Attributes
    ----------
    name : str
        The name of the institution
    city : str
        The city where the institution is located
    state : str
        The state where the institution is located
    latitude : float
        The latitude where the institution is located
    longitude : float
        The longitude where the institution is located
    """

    def __init__(self, name, city, state, latitude, longitude):
        """This method initializes the data members of the Institution class.

        Parameters
        ----------
        name : str
            The name of the institution
        city : str
            The city where the institution is located
        state : str
            The state where the institution is located
        latitude : float
            The latitude where the institution is located
        longitude : float
            The longitude where the institution is located
        """

        self.name = name
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        """Return a formated string representation of the class object"""

        return f"Institution({self.name})"

def append_institutions(schools, year, inst_name):
    """Add some extra institutions to the database of postsecondary schools

    Parameters
    ----------
    schools : GeoDataFrame
        The dataframe in which to append the new information
    year : int
        The year the postsecondary school information was collected
    inst_name : string
        The keyword to use when looking up the name of a school in the GeoDataFrame

    Returns
    -------
    GeoDataFrame
        The dataframe containing both the old and the new information
    """

    df2 = pd.DataFrame(
        {
            inst_name : [
                "Woods Hole Oceanographic Institution", "Arts et Metiers ParisTech", "University of Canterbury", "McGill University",
                "Trinity College Dublin", "Wilfrid Laurier University", "University of Melbourne", "University of Oxford",
                "Imperial College London", "National Tsing Hua University", "University of Toronto", "Pensacola Christian College",
                "University of Durham", "University of British Columbia", "Universidad de Antioquia", "University of Padua",
                "University of Bath", "University of Ottawa"
            ],
            "CITY" : [
                "Falmouth", "Paris", "Christchurch", "Montreal", "Dublin", "Waterloo", "Melbourne", "Oxford", "London", "Hsinchu City",
                "Toronto", "Pensacola", "Durham", "Vancouver", "Antioquia", "Padova PD", "Bath", "Ottawa"
            ],
            "STABBR" if year == 2015 else "STATE" : [
                "MA", "France", "New Zealand", "Canada", "Ireland", "Canada", "Australia", "United Kingdom", "United Kingdom",
                 "Taiwan", "Canada", "FL", "United Kingdom", "Canada", "Colombia", "Italy", "England", "Canada"
            ],
            "LAT1516" if year == 2015 else "LAT" : [
                41.524781001932716, 48.833508810585855, -43.52243692283857, 45.50543135620449,
                53.34434434753582, 43.474536145835756, -37.798583273349905, 51.75540084373608, 51.49896243904694,
                24.796345696985465, 43.661591621428244, 30.473591759462174, 54.765146814889256, 49.260822236130316,
                6.2689002766401485, 45.40693922363649, 51.378276373474485, 45.423279573514655
            ],
            "LON1516" if year == 2015 else "LON" : [
                -70.6711607, 2.358395261383819, 172.5800791301893, -73.57646445446471,
                -6.254485769308092, -80.5273405693174, 144.96136023807165, -1.2540234772696208, -0.174830586222553,
                120.99670208429329, -79.39612346136519, -87.23406222329352, -1.5780956131069162, -123.24589724211424,
                -75.56872258272178, 11.877499842431922, -2.326269953976108, -75.68311144407365
            ],
        },
    )
    schools = pd.concat([schools, df2], ignore_index = True, axis = 0)
    return schools

def get_institution(schools, home_institution, year, debug = False):
    """Find the correct postsecondary school in the database, store the relevant information in an Institution
    object, and return that object

    Parameters
    ----------
    schools : GeoDataFrame
        The dataframe containing information about postsecondary schools in the United States
    home_institution : str
        The name of the home institution for the program participant
    year : int
        The year the postsecondary school information was collected
    debug : bool, optional
        Prints extra information useful in debugging problems

    Returns
    -------
    Institution
        The Institution object containing the relevant data about the participants home institution
    """

    #pylint: disable=R0912

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
        for key, modifications in home_institution_secondary_replacements.items():
            if key in home_institution:
                # Cases: 1 = direct search, 2 = single replacement, 3 = prefix + replacement, 4 = double replacement
                if len(modifications) == 1:
                    institution = schools.loc[
                        schools[inst_name].isin(
                            [modifications[0]]
                        )
                    ]
                elif len(modifications) == 2:
                    institution = schools.loc[
                        schools[inst_name].isin(
                            [home_institution.replace(modifications[0], modifications[1])]
                        )
                    ]
                elif len(modifications) == 3:
                    institution = schools.loc[
                        schools[inst_name].isin(
                            [modifications[0] + home_institution.replace(modifications[1], modifications[2])]
                        )
                    ]
                elif len(modifications) == 4:
                    institution = schools.loc[
                        schools[inst_name].isin(
                            [home_institution.replace(modifications[0], modifications[1]).replace(modifications[2], modifications[3])]
                        )
                    ]
                break

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

def load_schools(year):
    """Load the correct database of postsecondary school locations

    Parameters
    ----------
    year : int
        The year the postsecondary school information was collected

    Returns
    -------
    GeoDataFrame
        A dataframe of school locations
    """

    schools = None
    if year == 2021:
        schools = gpd.read_file("data/schools/EDGE_GEOCODE_POSTSECONDARYSCH_CURRENT.shp")
    else:
        schools = gpd.read_file(f"data/schools/Postsecondary_School_Locations_{year}-{year - 1999}.shp")
    return schools
