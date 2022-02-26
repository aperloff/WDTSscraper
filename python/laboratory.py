#!/bin/env python3

"""laboratory

This module defines as class to store national laboratory information and a set of enums for the
DOE national laboratories involved in the STEM educational pipeline programs tracked by WDTS

Classes
----------
Laboratory
    Stores information about a single DOE national laboratory
Laboratories(ExtendedEnum)
    Sets enum aliases for each of the known DOE national laboratories
"""

from utilities import ExtendedEnum

class Laboratory:
    """A class which contains the information about a single laboratory.

    Attributes
    ----------
    name : str
        The name of the laboratory
    abbreviation : str
        The abbreviated name or initials of the laboratory
    city : str
        The city where the laboratory is located
    state : str
        The state where the laboratory is located
    latitude : float
        The latitude where the laboratory is located
    longitude : float
        The longitude where the laboratory is located

    Methods
    -------
    location
        Returns a formated string containing the city and state of the laboratory
    """

    def __init__(self, name, abbreviation, city, state, latitude, longitude):
        """This method initializes the data members of the Laboratory class.

        Parameters
        ----------
        name : str
            The name of the laboratory
        abbreviation : str
            The abbreviated name or initials of the laboratory
        city : str
            The city where the laboratory is located
        state : str
            The state where the laboratory is located
        latitude : float
            The latitude where the laboratory is located
        longitude : float
            The longitude where the laboratory is located
        """

        self.name = name
        self.abbreviation = abbreviation
        self.city = city
        self.state = state
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        """Return a formated string representation of the class object"""

        return f"Laboratory({self.name} ({self.abbreviation}))"

    def location(self):
        """Returns a formated string containing the city and state of the laboratory"""

        return f"{self.city}, {self.state}"

class Laboratories(ExtendedEnum):
    """Enumerate the DOE national laboratories

    Latitude and longitude values found using:
        1. https://www.findlatitudeandlongitude.com/find-latitude-and-longitude-from-address/
        2. https://www.latlong.net/
        3. https://www.maps.google.com
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
        """Return a formated string representation of the class object"""

        return f"<{self.__class__.__name__}.{self.name}: {self.value.__repr__()}>"
