#!/usr/bin/env python3

"""This module contains the pytest tests for the modules:
    1. WDTSscraper.py
    2. check_for_dependencies.py
    3. institution.py
    4. laboratory.py
    5. pdf_parsers.py
    6. person.py
    7. utilities.py

    Note: The plotter code is not tested as we haven't figured out a good way to test the output for consistency
    Note: you can use the decorator '@pytest.mark.skip(reason="taskes a long time to run")' to skip over a test
"""

from __future__ import absolute_import
import glob
import os
import sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__))+'/../python/')
# pylint: disable=wrong-import-position
import check_for_dependencies
import institution
import laboratory
import pdf_parsers
import person
import utilities
import WDTSscraper
# pylint: enable=wrong-import-position
# pylint: disable=no-self-use

class TestCheckForDependencies:
    """Class containing the tests for the check_for_dependencies module.
    We want to make sure that the checks for the dependencies will work.
    """

    def test_is_tool(self):
        """Check for a common executable to see if this function even works"""

        assert check_for_dependencies.is_tool("ls")

    def test_check_pip_dependencies(self):
        """Check if we can test for the most basic of pip installed dependencies"""

        dep = {"numpy" : ["pip"]}
        assert len(check_for_dependencies.check_pip_dependencies(dep)) == 0

    def test_check_try_dependencies(self):
        """Check if we can test for the most basic of python modules"""

        dep = ["os","sys"]
        assert len(check_for_dependencies.check_try_dependencies(dep)) == 0

    def test_check_system_dependencies(self):
        """Check if we can test for simple system installed dependencies"""

        dep = ["ls"]
        assert len(check_for_dependencies.check_system_dependencies(dep)) == 0

class TestInstitution:
    """Class containing the tests for the institution module."""

    def test_load_schools(self):
        """Tests the ability to load a database of postsecondary school locations"""

        year= 2021
        inst_name = "NAME"
        schools = institution.load_schools(year)
        assert schools.iloc[-1][inst_name] == "Zorganics Institute Beauty and Wellness"

    def test_append_institutions(self):
        """Tests the ability to append a set of values to the database of postsecondary school locations"""

        year = 2021
        inst_name = "NAME"
        schools = institution.load_schools(year)
        schools = institution.append_institutions(schools, year, inst_name)
        school = schools.loc[schools[inst_name].isin(["University of Melbourne"])]
        assert not school.empty
        assert school.iloc[0][inst_name] == "University of Melbourne"

    def test_institution(self):
        """Tests the Institution class to make sure that it's attributes are set correctly"""

        inst = institution.Institution("University of Melbourne", "Melbourne", "Australia", -37.798583273349905, 144.96136023807165)
        assert inst.name == "University of Melbourne" and \
               inst.city == "Melbourne" and \
               inst.state == "Australia" and \
               inst.latitude == -37.798583273349905 and \
               inst.longitude == 144.96136023807165

    def test_get_institution(self):
        """Tests the ability to form an Insitution object based on the name of the institution"""

        year = 2021
        schools = institution.load_schools(year)
        inst = institution.get_institution(schools, "University of Melbourne", year)
        assert inst.name == "University of Melbourne" and \
               inst.city == "Melbourne" and \
               inst.state == "Australia" and \
               inst.latitude == -37.798583273349905 and \
               inst.longitude == 144.96136023807165

class TestLaboratory:
    """Class containing the tests for the laboratory module."""

    def test_laboratory(self):
        """Tests the Laboratory class to make sure that it's attributes are set correctly"""

        lab = laboratory.Laboratory("Fermi National Accelerator Laboratory", "FNAL", "Batavia", "IL", 41.845584, -88.230627)
        assert lab.name == "Fermi National Accelerator Laboratory" and \
               lab.abbreviation == "FNAL" and \
               lab.city == "Batavia" and \
               lab.state == "IL" and \
               lab.latitude == 41.845584 and \
               lab.longitude == -88.230627
        assert lab.location() == "Batavia, IL"

    def test_laboratories(self):
        """Tests the Laboratories class by checking the list of names and values."""

        assert laboratory.Laboratories.list_names() == [
            laboratory.Laboratories.AMES.name,
            laboratory.Laboratories.ANL.name,
            laboratory.Laboratories.BNL.name,
            laboratory.Laboratories.DNR.name,
            laboratory.Laboratories.FNAL.name,
            laboratory.Laboratories.GA_DIII_D.name,
            laboratory.Laboratories.INL.name,
            laboratory.Laboratories.LBNL.name,
            laboratory.Laboratories.LLNL.name,
            laboratory.Laboratories.LANL.name,
            laboratory.Laboratories.NREL.name,
            laboratory.Laboratories.NETL.name,
            laboratory.Laboratories.ORNL.name,
            laboratory.Laboratories.PNNL.name,
            laboratory.Laboratories.PPPL.name,
            laboratory.Laboratories.SNL_CA.name,
            laboratory.Laboratories.SNL_NM.name,
            laboratory.Laboratories.SRNL.name,
            laboratory.Laboratories.SLAC.name,
            laboratory.Laboratories.TJNAF.name,
        ]
        assert laboratory.Laboratories.list_values()[0].name == \
               laboratory.Laboratory("Ames National Laboratory","AMES","Ames","IA",42.02997,-93.648319).name

class TestPDFParsers:
    """Class containing the tests for the pdf_parsers module."""

    # pylint: disable=C0103

    def test_handle_known_issues_parsing_input(self):
        """Test the ability of the handle_known_issues_parsing_input() function to return the correct values"""

        lines = [[
            "VFP",
            "Ouango, Boinzemwende Jarmila RoxaHostos Community College‐City University of New York",
            "Brookhaven National Laboratory (BNL)",
            "High Energy Physics"
        ]]
        lines_fixed = [[
            "VFP",
            "Ouango, Boinzemwende Jarmila Roxane",
            "Hostos Community College‐City University of New York",
            "Brookhaven National Laboratory (BNL)",
            "High Energy Physics"
        ]]
        year = 2021
        assert pdf_parsers.handle_known_issues_parsing_input(lines = lines, year = year) == lines_fixed

    def test_process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic(self):
        """Test the process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic() function to parse the 2021 WDTS input file"""

        ref_people = [
            person.Person("VFP", "Faculty", " Osama \"Sam\"", "Abuomar", "Lewis University", "ANL", "Information Sciences", 2021),
            person.Person("VFP", "Student", " Ricardo", "Zamora", "St. Mary's University", "LBNL", "Computational Sciences", 2021),
        ]
        people = pdf_parsers.process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic(
            "data/VFP/WDTS-SULI-CCI-VFP-Summer-2021.pdf",
            2021
        )
        assert people[0].participant() == ref_people[0].participant() and people[-1].participant() == ref_people[-1].participant()

    def test_process_file_table_no_lines_term_lastname_firstname_institution_laboratory(self):
        """Test the process_file_table_no_lines_term_lastname_firstname_institution_laboratory() function to parse the 2020 VFP input file"""

        ref_people = [
            person.Person("VFP", "Faculty", "Osama \"Sam\"", "Abuomar", "Lewis University", "ANL", "", 2020),
            person.Person("VFP", "Faculty", "Haiyan", "Zhao", "Univeristy of Idaho-Idaho Falls", "INL", "", 2020),
        ]
        people = pdf_parsers.process_file_table_no_lines_term_lastname_firstname_institution_laboratory("data/VFP/2020-VFP-F-participants.pdf", 2020)
        assert people[0].participant() == ref_people[0].participant() and people[-1].participant() == ref_people[-1].participant()

    def test_process_file_table_with_lines_name_institution_laboratory_term(self):
        """Test the process_file_table_with_lines_name_institution_laboratory_term() function to parse the 2020 VFP input file"""

        ref_people = [
            person.Person("VFP", "Faculty", "Paul", "Akangah", "North Carolina Agricultural and Technical State University", "BNL", "", 2019),
            person.Person("VFP", "Faculty", "Cheng", "Zhang", "LIU Post", "BNL", "", 2019),
        ]
        people = pdf_parsers.process_file_table_with_lines_name_institution_laboratory_term("data/VFP/VFP-F-participants-2019.pdf", 2019)
        assert people[0].participant() == ref_people[0].participant() and people[-1].participant() == ref_people[-1].participant()

    def test_process_file_table_with_lines_name_institution_laboratory_area(self):
        """Test the process_file_table_with_lines_name_institution_laboratory_area() function to parse the 2015 VFP input file"""

        ref_people = [
            person.Person(
                "VFP",
                "Faculty",
                "Marcus",
                "Allfred",
                "Howard University",
                "BNL",
                "",
                2015
            ),
            person.Person("VFP",
                "Faculty",
                "Zhijun",
                "Zhan",
                "North Carolina Agricultural and Technical State University",
                "ORNL",
                "",
                2015
            ),
        ]
        people = pdf_parsers.process_file_table_with_lines_name_institution_laboratory_term(
            "data/VFP/2015-VFP-Faculty-Terms_Participant-Report.pdf",
            2015
        )
        assert people[0].participant() == ref_people[0].participant() and people[-1].participant() == ref_people[-1].participant()

class TestPerson:
    """Class containing the tests for the person module."""

    def test_jobs(self):
        """Tests the Jobs class by checking the list of names and values."""

        assert person.Jobs.list_names() == [person.Jobs.Staff.name, person.Jobs.Scientist.name, person.Jobs.Faculty.name, person.Jobs.Engineer.name,
                                            person.Jobs.Postdoc.name, person.Jobs.Student.name, person.Jobs.Unknown.name]
        assert person.Jobs.list_values() == ["Staff", "Scientist", "Faculty", "Engineer", "Postdoc", "Student", "Unknown"]

    def test_person(self):
        """Tests the Person class to make sure that it's attributes are set correctly"""

        jane = person.Person("program", "job", "jane", "doe", "home_inst", "host_lab", "HEP", 9999)

        assert jane.program == "program" and \
               jane.job == "job" and \
               jane.first_name == "jane" and \
               jane.last_name == "doe" and \
               jane.home_institution == "home_inst" and \
               jane.host_doe_laboratory == "host_lab" and \
               jane.topic == "HEP" and \
               jane.year == 9999
        assert jane.participant() == "doe, jane"

class TestUtilities:
    """Class containing the tests for the utilities module."""

    def test_extended_enum_list_names(self):
        """Tests the ExtendedEnum class by checking the list_names() member function."""

        class Color(utilities.ExtendedEnum):
            """Dummy class for testing utilities.ExtendedEnum"""

            RED = 'RED'
            GREEN = 'GREEN'
            BLUE = 'BLUE'

        assert Color.list_names() == ['RED', 'GREEN', 'BLUE']

    def test_extended_enum_list_values(self):
        """Tests the ExtendedEnum class by checking the list_values() member function."""

        class Color(utilities.ExtendedEnum):
            """Dummy class for testing utilities.ExtendedEnum"""

            RED = 'RED'
            GREEN = 'GREEN'
            BLUE = 'BLUE'

        assert Color.list_values() == ['RED', 'GREEN', 'BLUE']

    def test_filter_people_by_topic(self):
        """Tests the filter_people_by_topic function from within the utilities module."""

        names = ["alice", "bob", "john", "mary"]
        topics = ["HEP", "High Energy Physics", "Biophysics", ""]
        people = [person.Person("program", "job", name, "last_name", "home_inst", "host_lab", topics[iname], 9999) for iname,name in enumerate(names)]

        group1 = utilities.filter_people_by_topic(people, False, ["HEP"])
        group2 = utilities.filter_people_by_topic(people, False, ["HEP", "High Energy Physics"])
        group3 = utilities.filter_people_by_topic(people, True, ["HEP"])

        assert any(person.first_name == "alice" for person in group1) and len(group1) == 2
        assert any(person.first_name == "mary" for person in group1) and len(group1) == 2
        assert not any(person.first_name == "bob" for person in group1) and len(group1) == 2
        assert any(person.first_name == "bob" for person in group2) and len(group2) == 3
        assert any(person.first_name == "alice" for person in group3) and len(group3) == 1
        assert not any(person.first_name == "mary" for person in group3) and len(group3) == 1

class TestWDTSscraper:
    """This section covers the integration tests.
    These tests will make sure that all of the code works in harmony.
    """

    def test_wdts_scraper(self):
        """Performs a check on the main function of the code.
        In the end we will be making sure that an image file is created.
        """

        WDTSscraper.wdts_scraper(['-C','python/configs/config_all_programs_2021.py'])
        files = glob.glob('*_map_v*.*')
        print("TestWDTSscraper::test_wdts_scraper() Found the files: " + str(files))
        assert len(files) > 0
