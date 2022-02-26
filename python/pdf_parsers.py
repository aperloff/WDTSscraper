#!/bin/env python3

"""pdf_parsers

This module contains functions which are involved in parsing a PDF file containing a list of program participants and some accompanying information

Functions
---------
handle_known_issues_parsing_input
    Corrects some known issues when parsing the PDF files (kind of like an empirical catch-all function)
process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic
    Returns a list of program participants by parsing a PDF file
process_file_table_no_lines_term_lastname_firstname_institution_laboratory
    Returns a list of program participants by parsing a PDF file
process_file_table_with_lines_name_institution_laboratory_term
    Returns a list of program participants by parsing a PDF file
process_file_table_with_lines_name_institution_laboratory_area
    Returns a list of program participants by parsing a PDF file
"""

import operator

import pdfplumber

from institution import get_institution
from institution import load_schools
from laboratory import Laboratories
from person import Person
from person import Jobs

def handle_known_issues_parsing_input(lines, year, debug = False):
    """Corrects some known issues when parsing the PDF files (kind of like an empirical catch-all function)

    Parameters
    ----------
    lines : list
        A list of lists of strings containing the text from the PDF file, broken up by row and then column
    year : int
        The year the program took place
    debug : bool, optional
        Print extra information useful for debugging issues

    Returns
    -------
    list
        The corrected list of lines
    """

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

def process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic(filename, year, debug = False, program_filter = None, sort = True):
    """Parses a PDF file containing a table with no dividing lines and containing the following columns of information:
        - Abbreviated program name
        - The participant's last and first name
        - The participant's home institution
        - The national laboratory which hosted the participant
        - The topic of the research

    Parameters
    ----------
    filename : str
        A string containing the path to the PDF file
    year : int
        The year the program took place
    debug : bool, optional
        Print extra information useful for debugging issues
    program_filter : list, optional
        A list of strings containing the programs to select for, in case the PDF contains information about multiple programs
    sort : bool, optional
        Sort the resulting list of people by job classification ("Faculty", "Student", etc.)

    Returns
    -------
    list
        A list of Person objects containing the information obtained from the PDF file
    """

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
    """Parses a PDF file containing a table with no dividing lines and containing the following columns of information:
        - The term (`season year`) in which the program took place
        - The participant's last
        - The participant's first name
        - The participant's home institution
        - The national laboratory which hosted the participant

    Parameters
    ----------
    filename : str
        A string containing the path to the PDF file
    year : int
        The year the program took place
    debug : bool, optional
        Print extra information useful for debugging issues
    program_filter : list, optional
        A list of strings containing the programs to select for, in case the PDF contains information about multiple programs
    sort : bool, optional
        Sort the resulting list of people by job classification ("Faculty", "Student", etc.)

    Returns
    -------
    list
        A list of Person objects containing the information obtained from the PDF file
    """

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
    """Parses a PDF file containing a table with dividing lines and containing the following columns of information:
        - The participant's full name
        - The participant's home institution
        - The national laboratory which hosted the participant
        - The season in which the program took place (i.e. Summer, Fall, etc.)

    Parameters
    ----------
    filename : str
        A string containing the path to the PDF file
    year : int
        The year the program took place
    debug : bool, optional
        Print extra information useful for debugging issues
    program_filter : list, optional
        A list of strings containing the programs to select for, in case the PDF contains information about multiple programs
    sort : bool, optional
        Sort the resulting list of people by job classification ("Faculty", "Student", etc.)

    Returns
    -------
    list
        A list of Person objects containing the information obtained from the PDF file
    """

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
    """Parses a PDF file containing a table with dividing lines and containing the following columns of information:
        - The participant's full name
        - The participant's home institution
        - The national laboratory which hosted the participant
        - The topic of the research

    Parameters
    ----------
    filename : str
        A string containing the path to the PDF file
    year : int
        The year the program took place
    debug : bool, optional
        Print extra information useful for debugging issues
    program_filter : list, optional
        A list of strings containing the programs to select for, in case the PDF contains information about multiple programs
    sort : bool, optional
        Sort the resulting list of people by job classification ("Faculty", "Student", etc.)

    Returns
    -------
    list
        A list of Person objects containing the information obtained from the PDF file
    """

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
