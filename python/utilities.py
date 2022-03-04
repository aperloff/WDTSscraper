#!/bin/env python3

"""utilties

This module provides some needed extensions used by the WDTSscraper and its associated modules.

Classes
----------
ExtendedEnum(Enum)
    An extension to the Enum class which adds some class methods

Functions
---------
filter_people_by_topic(people, strict = False)
    Filters the list of People by their research topic(s)
"""

from datetime import date
from enum import Enum
import os

class ExtendedEnum(Enum):
    """An extension to the Enum class

    From: https://stackoverflow.com/questions/29503339/how-to-get-all-values-from-python-enum-class

    Methods
    -------
    list_names(cls)
        Returns a list of the names in the Enum class
    list_values(cls)
        Returns a list of the values in the Enum class
    """

    @classmethod
    def list_names(cls):
        """Returns a list of the names in the Enum class"""

        return list(map(lambda c: c.name, cls))

    @classmethod
    def list_values(cls):
        """Returns a list of the values in the Enum class"""

        return list(map(lambda c: c.value, cls))

def filter_people_by_topic(people, strict = False, topics = None):
    """Filter the list of people by their research topic(s)

    Parameters
    ----------
    people : list
        A list of Person objects (or objects with a 'topic' attribute)
    strict : bool, optional
        If strict is True, then this function also removes people whith no topic stored
    topics : list, optional
        A list of keyword strings that must be present in the research topic in order for the person to be kept

    Returns
    -------
    list
        A filtered list of people

    Raises
    ------
    TypeError
        If topics is not None, then it is expected to be a list of strings, not a string.
    """

    if not isinstance(topics, list):
        raise TypeError("ERROR::filter_people_by_topic() The 'topics' argument must be a list of strings.")

    return [person for person in people if (not strict and not person.topic) or (topics is not None and any(t in person.topic for t in topics))]

def get_formatted_filename(path, filename, fmt):
    """Determine a filename based on the current date and any already existing files.

    The current date will be prepended to the filename and a version number will be added to the end, just before the file extension.
    The version is determined by looking to see if a file already exists for a given version number. The code starts by looking for
    'v0' and the sequentially increments the number until there is no pre-existing file. This is the version number which will be given
    to the resulting filename. This feature is most useful for naming output files.

    Parameters
    ----------
    path : str
        The path to the directory which contains or will contain the file
    filename : str
        The main part of the filename, which will have a prefix and a suffix appended to it
    fmt : str
        The extension of the file

    Returns
    -------
    str
        A formated string containing the filename
    """

    if path and path[-1] != "/":
        path += "/"
    output_filename = f"{path}{date.today().strftime('%Y_%m_%d')}_{filename}"
    i = 0
    while os.path.exists(f"{output_filename}_v{i}.{fmt}"):
        i += 1
    return f"{output_filename}_v{i}.{fmt}"
