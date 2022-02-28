#!/usr/bin/env python3

"""This module contains the pytest tests for the modules:
    1. WDTSscraper.py
    2. check_for_dependencies.py
    3. institution.py
    4. laboratory.py
    5. pdf_parsers.py
    6. person.py
    7. plotter.py
    8. utilities.py

    Note: you can use the decorator '@pytest.mark.skip(reason="taskes a long time to run")' to skip over a test
"""

from __future__ import absolute_import
from io import StringIO
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/../python/')
# pylint: disable=wrong-import-position
import pytest # pylint: disable=import-error
import WDTSscraper
import check_for_dependencies
import institution
import laboratory
import pdf_parsers
import person
import plotter
import utilities
# pylint: enable=wrong-import-position
# pylint: disable=no-self-use

class Capturing(list):
    """A context manager which captures stdout and returns it as a list of strings, one for each line.
    This class is based on https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call

    Example use:
        with Capturing() as output:
            <Some code that usually prints to sys.stdout>
        print(output)    
    """

    def __enter__(self):
        # pylint: disable=attribute-defined-outside-init
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

#class TestWDTSscraper:
#class TestCheckForDependencies:
#class TestInstitution:
#class TestLaboratory:
#class TestPDFParsers:
#class TestPerson:
#class TestPlotter:

class TestUtilities:
    """Class containing the tests for the utilities module."""

    def test_extended_enum_list_names(self):
        """Tests the ExtendedEnum class by checking the list_names() member function."""
        class Color(utilities.ExtendedEnum):
            RED = 'RED'
            GREEN = 'GREEN'
            BLUE = 'BLUE'

        assert Color.list_names() == ['RED', 'GREEN', 'BLUE']

    def test_extended_enum_list_values(self):
        """Tests the ExtendedEnum class by checking the list_values() member function."""
        class Color(utilities.ExtendedEnum):
            RED = 'RED'
            GREEN = 'GREEN'
            BLUE = 'BLUE'

        assert Color.list_values() == ['RED', 'GREEN', 'BLUE']

    #def test_filter_people_by_topic(self):
        """Tests the """