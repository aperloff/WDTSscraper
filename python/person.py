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

from utilities import ExtendedEnum

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
