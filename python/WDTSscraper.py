#!/bin/env python3

"""WDTSscraper

This script allows the user to create a map of the United States showing participation in the WDTS tracked
DOE educational pipeline research programs. On top of the US map will be the locations of the home institutions
of the participants and the national labs where the research programs take place. The user has the option
to draw lines connecting the two sites.

Functions
---------
WDTSscraper
    The main function of the script
"""

from argparse import RawTextHelpFormatter
import os
import sys

from magiconfig import ArgumentParser, MagiConfigOptions

from pdf_parsers import process_file_table_no_lines_program_lastfirstname_institution_laboratory_topic
from pdf_parsers import process_file_table_no_lines_term_lastname_firstname_institution_laboratory
from pdf_parsers import process_file_table_with_lines_name_institution_laboratory_term
from pdf_parsers import process_file_table_with_lines_name_institution_laboratory_area
from plotter import plot_map
from utilities import filter_people_by_topic

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
    """The main function for this scrip

    Parameters
    ----------
    debug : bool, optional
        Prints additional information necessary to debug this script and the other modules in this package
    files : list, optional
        Alist of strings with paths to the PDF files provided by WDTS that the pdf_parser module should used to gather information
    filter_by_topic : bool, optional
        If True, the list of people will be filtered by their research topic
    formats : list, optional
        List of string formats with which to save the resulting map
    interactive : bool, optional
        Show the plot during program execution
    no_draw : bool, optional
        If True, the map will not be created or saved
    no_lines : bool, optional
        If True, the the lines connecting the home institutions and the national laboratories will not be drawn
    output_path : str, optional
        The path to the directory in which to save the resulting maps
    strict_filtering : bool, optional
        More tightly filter out participants by removing those whose topic is unknown
    types : list, optional
        A list of strings containing the types of files (DOE program abbreviations) being processed
    years : list, optional
        A list of int representing the year of the program, which helps determine how to process each file
    """

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
        people = filter_people_by_topic(people, strict = strict_filtering, topics = ["HEP", "High Energy Physics"])

    if not no_draw:
        plot_map(
            debug = debug,
            formats = formats,
            lines = not no_lines,
            output_path = output_path,
            person_data = people,
            show = interactive,
            states = None,
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
