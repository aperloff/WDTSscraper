#!/bin/env python3

"""person

This module defines classes which store information about an individual person and their job classification

Classes
----------
Jobs(ExtendedEnum)
    Sets enum aliases for each of the known job classifications
Person
    Stores information about a person who participated in one of the programs tracks by WDTS
"""

import os

import jsons
from magiconfig import MagiConfig

from laboratory import Laboratories
from institution import Institution
from utilities import ExtendedEnum, get_formatted_filename

class Jobs(ExtendedEnum):
    """Enumerate the job classifications"""

    # pylint: disable=C0103
    Staff = "Staff"
    Scientist = "Scientist"
    Faculty = "Faculty"
    Engineer = "Engineer"
    Postdoc = "Postdoc"
    Student = "Student"
    Unknown = "Unknown"

class Person:
    """A class which contains the information about a single person.

    Attributes
    ----------
    program : str
        The name of the DOE program in which the person participated
    job : Job
        The job held by the person during the term of the program
    first_name : str
        The person's first name
    last_name : str
        The person's last name
    home_institution : str
        The name of the person's home institution
    host_doe_laboratory : str
        The name of the laboratory where the research project took place
    topic : str
        The topic of the research project
    year : int
        The year the program took place

    Methods
    -------
    participant
        Returns a formated string containing the first and last names of the Person
    """

    def __init__(self, program, job, first_name, last_name, home_institution, host_doe_laboratory, topic, year):
        """This method initializes the data members of the Person class.

        Parameters
        ----------
        program : str
            The name of the DOE program in which the person participated
        job : Job
            The job held by the person during the term of the program
        first_name : str
            The person's first name
        last_name : str
            The person's last name
        home_institution : str
            The name of the person's home institution
        host_doe_laboratory : str
            The name of the laboratory where the research project took place
        topic : str
            The topic of the research project
        year : int
            The year the program took place
        """

        self.program = program
        self.job = job
        self.first_name = first_name
        self.last_name = last_name
        self.home_institution = home_institution
        self.host_doe_laboratory = host_doe_laboratory
        self.topic = topic
        self.year = year

    def __repr__(self):
        """Return a formated string representation of the class object"""

        return (
            f"Person({self.program} | {self.job} | {self.participant()} | {self.home_institution} | "
            f"{self.host_doe_laboratory.__repr__()} | {self.topic} | {self.year})"
        )

    def participant(self):
        """Return a formated string containing the first and last names of the Person"""

        return f"{self.last_name}, {self.first_name}"

def get_people(files, types, years, process_file_map, debug = False):
    """This function first determines the input file type (pdf or txt) and then figures out how to parse that file
    to find a list of participant names. If it's a pdf file, then the code will call one of the pdf parsers. If the file
    is a serialized list of people, then it will call the necessary functions to deserialize the list.

    Parameters
    ----------
    files : list
        A list of strings containing the path to the input files
    types : list
        A list of strings containing the initials of the programs represented (must be one of the available options)
    years : list
        A list of integer years that the programs took place (can be anything if reading from a txt file)
    process_file_map : dict
        A dictionary of parser functions whose key is a tuple of (program, year)
    debug : bool
        Print extra information useful for debugging issues
    """

    people = []
    for ifilename, filename in enumerate(files):
        _, file_extension = os.path.splitext(filename)

        if file_extension == ".pdf":
            if years[ifilename] <= 2014:
                raise RuntimeError("Unfortunately we are unable to get university/institution locations for any year prior to 2015.")
            if file_extension == ".pdf" and (types[ifilename], years[ifilename]) not in process_file_map:
                raise RuntimeError(f"We don't know how to process {types[ifilename]} files for the year {years[ifilename]}.")

            print(f"Processing the file {filename} (year = {years[ifilename]}, program = {types[ifilename]}) ... ")
            people += process_file_map[(types[ifilename], years[ifilename])](
                filename,
                years[ifilename],
                debug = debug,
                program_filter = [types[ifilename]]
            )
        elif file_extension == ".txt":
            print(f"Processing the file {filename} ... ")
            with open(filename, "r", encoding="utf8") as file:
                header = read_header(file)
                config = jsons.loads(' '.join(header.split()), MagiConfig)
                for isubfilename, subfilename in enumerate(config.files):
                    print(f"\tContains people from {subfilename} (year = {config.years[isubfilename]}, program = {config.types[isubfilename]})")
                people = read_people(file)
                if debug:
                    print(people)
        else:
            raise RuntimeError(f"Uh oh! We don't know how to read a '{file_extension}' file.")
    return people

def read_header(file, delimiter = "#"):
    """Read the header for an open file

    Parameters
    ----------
    file : _io.TextIOWrapper
        The open file object
    delimiter : str, optional
        The string at the begining of a line which denotes that it's part of the header
    """

    header = ""
    last_pos = file.tell()
    line = file.readline()
    while line[0 : len(delimiter)] == delimiter:
        header += line[len(delimiter) : ]
        last_pos = file.tell()
        line = file.readline()
    file.seek(last_pos)
    return header

def read_people(file, delimiter = "#", header_removed = False):
    """Read a list of people from a text file.

    It is assumed, though not required, that the text file will begin with a header which is denoted by
    contiguous lines beginning with a '#'. The rest of the file will be read and deserialized as a list of
    Person objects.

    Parameters
    ----------
    file : _io.TextIOWrapper
        The open file object
    delimiter : str, optional
        The string at the begining of a line which denotes that it's part of the header
    header_removed : bool, optional
        If set to False (default), then the code will try to remove the header.
    """

    if not header_removed:
        _ = read_header(file, delimiter)
    lines = file.readlines()
    list_people = jsons.loads(''.join(lines))
    deserialized_people  = []
    for person in list_people:
        deserialized_people.append(jsons.load(person, Person))
        deserialized_people[-1].job = jsons.load(deserialized_people[-1].job, Jobs)
        deserialized_people[-1].home_institution = jsons.load(deserialized_people[-1].home_institution, Institution)
        deserialized_people[-1].host_doe_laboratory = jsons.load(deserialized_people[-1].host_doe_laboratory, Laboratories)
    return deserialized_people

def save_people(arguments, people):
    """Save the list of people to a text file for later review or analysis.

    Each Person object will be JSON serialized and then written to a text file. The file will also contain a header which shows
    the MagicConfig arguments used to create the list of people. This is there so that the list can be recreated if needed.

    Parameters
    ----------
    arguments : MagicConfig
        The complete list of MagicConfig arguments
    people : list
        A list of Person objects
    """

    output_filename = get_formatted_filename(arguments.output_path, "people", "txt")
    with open(output_filename, "w", encoding="utf8") as file:
        # Write a header to the file
        header = jsons.dumps(arguments, jdkwargs={'indent' : 4, 'sort_keys' : False})
        for line in header.split("\n"):
            file.write(f"#{line}\n")

        #for person in people:
        #    serialized_person = jsons.dumps(person, jdkwargs={'indent' : 4, 'sort_keys' : False})
        #    file.write(f"{serialized_person}\n")
        serialized_people = jsons.dumps(people, jdkwargs={'indent' : 4, 'sort_keys' : False})
        file.write(f"{serialized_people}")
