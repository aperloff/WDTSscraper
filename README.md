# WDTSscraper

[![Lint Code](https://github.com/aperloff/WDTSscraper/actions/workflows/lint.yml/badge.svg)](https://github.com/aperloff/WDTSscraper/actions/workflows/lint.yml) [![Deploy images](https://github.com/aperloff/WDTSscraper/actions/workflows/deploy_images.yml/badge.svg)](https://github.com/aperloff/WDTSscraper/actions/workflows/deploy_images.yml)

Scrape [US Department of Energy (DOE)](https://www.energy.gov/) [Office of Science](https://science.osti.gov/) [Workforce Development for Teachers and Scientists (WDTS)](https://science.osti.gov/wdts) produced PDF files for information about DOE run STEM pipeline programs. The information is taken from [WDTS](https://science.osti.gov/wdts), the [US Census Bureau](https://www.census.gov/), and the [US Department of Education](https://www.ed.gov/). 

The currently list of STEM pipeline programs whose information can be gathered and parsed are:
  - [Community College Internships (CCI)](https://science.osti.gov/wdts/cci)
  - [Office of Science Graduate Student Research (SCGSR) Program](https://science.osti.gov/wdts/scgsr)
  - [Science Undergraduate Laboratory Internships (SULI)](https://science.osti.gov/wdts/suli)
  - [Visiting Faculty Program (VFP)](https://science.osti.gov/wdts/vfp)

To report a bug or request a feature, please [file an issue](https://github.com/aperloff/WDTSscraper/issues/new/choose).

Table of Contents
=================
<!-- MarkdownTOC autolink="true" -->

- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Available Docker Images](#available-docker-images)
- [Command Line Interface](#command-line-interface)
  - [Basic example](#basic-example)
  - [Options](#options)
  - [Tools](#tools)
- [Using Docker](#using-docker)
- [Examples](#examples)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
  - [Unit Testing](#unit-testing)
    - [Bats for Bash scripts](#bats-for-bash-scripts)
    - [Pytest for Python modules](#pytest-for-python-modules)
  - [Linting](#linting)
- [Acknowledgments / Contributors](#acknowledgments--contributors)

<!-- /MarkdownTOC -->

## Installation

### Local Installation
If you wish to install the dependencies yourself and only wish to checkout the code and download the needed input data, then you may use the following commands.

```bash
git clone git@github.com:aperloff/WDTSscraper.git
data/download.sh
```

If the necessary input files were downloaded correctly you should see some output which looks like:

```
Creating the directory data/us_map ... DONE
Creating the directory data/schools ... DONE
Creating the directory data/CCI ... DONE
Creating the directory data/SCGSR ... DONE
Creating the directory data/SULI ... DONE
Creating the directory data/VFP ... DONE
Downloading the US map information ... DONE, VERIFIED
Extracting the US map shapefiles ... DONE
Downloading information about US postsecondary schools ... DONE, VERIFIED
Extracting the school information ... DONE
Downloading the list of CCI participants ... DONE, VERIFIED
Downloading the list of SCGSR participants ... DONE, VERIFIED
Downloading the list of SULI participants ... DONE, VERIFIED
Downloading the list of VFP participants ... DONE, VERIFIED

SUCCESS::All files downloaded!
```

### Available Docker Images

If you'd rather use a clean environment, there is an available set of Docker image ([aperloff/wdtsscraper](https://hub.docker.com/r/aperloff/wdtsscraper)) with the following tags:

  - `latest`: Contains all of the necessary dependencies and the WDTSscraper code. This image does not contain any of the necessary input data.
  - `latest-data`: Contains everything in the `latest` image, but also contains the input data.
  
Further information about using these images will be given below (see [Using Docker](#using-docker)).

## Command Line Interface

### Basic example

```python
python3 python/WDTSscraper.py -C python/configs/config_all-programs_2021.py
```

The output will be an image file.

### Options

The command line options available are:

  - `-d, --debug`: Shows some extra information in order to debug this program (default = False)
  - `-f, --files [files]`: The absolute paths to the files to scrape
  - `-F, --formats [formats]`: List of formats with which to save the resulting map (choices = [`png`,`pdf`,`ps`,`eps`,`svg`], default = [`png`])
  - `-i, --interactive`: Show the plot during program execution
  - `-n, --no-lines`: Do not plot the lines connecting the home institutions and the national laboratories
  - `-N, --no-draw`: Do not create or save the resulting map
  - `-O, --output-path=OUTPUTPATH`: Directory in which to save the resulting maps (default = `os.cwd()`)
  - `-S, --strict-filtering`: More tightly filter out participants by removing those whose topic is unknown
  - `-t, --types [types]`: A list of the types of files being processed (choices = [`VFP`,`SULI`,`CCI`,`SCGSR`])
  - `-T, --filter-by-topic`: Filter the participants by topic if the topic is available
  - `-y, --years [years]`: A list of years to help determine how to process each file

The number of files, types, and years must be equal (i.e. you can't specify 10 input files and years, but only 9 program names).

### Tools

There are two tools used for managing the input data collected from the US government:

  - `data/download.sh`: This is used for downloading and extracting the entire collection of needed input files. It gathers US map information from the Census Bureau, post-secondary school information from the Department of Education, and DOE program participation from WDTS.
  - `data/clean.sh`: This will remove all sub-directories within the `data/` directory. This effectively wipes the slate clean. Make sure not to store any valuable files within these sub-directories.

## Using Docker

There are a few workflows available when using the Docker images:

1. You may choose to use the `latest` image as a clean environment, but download up-to-date input files. In this case, you will need to run the `data/download.sh` script manually.
2. You may choose to use the `latest-data` image, which already contains the input data. In this case, you will only need to run `python/WDTSscraper.py`
3. An alternative mode has you checkout the code and download the input data locally, but use one of the Docker images to provide the necessary dependencies. In this case, the code and input data within the image will automatically be replaced by your local version using a bind mount. This method is most useful for people wishing to develop a new feature for the repository, but who want to avoid installing the dependencies on their local machine. The resulting images will be copied back to the host machine. To run in this mode, a helper script has been developed to wrap up all of the Docker complexities. Simply run:

    ```bash
    .docker/run.sh -C python/configs/config_all_programs_2021.py
    ```
    **Note**: To use this running mode, you will need to have permission to bind mount the local directory and the local user will need permission to write to that directory as well. This is typically not a problem unless the repository has been checked out inside a restricted area of the operating system or the permissions on the directory have been changed.

## Examples

Here are some examples of the types of images which can be created.

The first one displays the DOE national laboratories involved in the VFP, the home institutions for the faculty and students involved, and the connections between those home institutions and the national laboratories. The plot covers from 2015 to 2021 and includes all research areas.

![VFP connections 2015-2021](examples/VFP_2015-2021.png "VFP connections 2015-2021")

The second image shows the DOE national laboratories and home institutions involved in the CCI, SCGSR, SULI, and VFP programs, but only for students and faculty verifiably involved in high energy physics (HEP) research. Because there was no information about the type of research being done by CCI participants, there are no makers on the plot for that programs. Once again this plot covers from 2015 to 2021.

![HEP pipeline programs 2015-2021](examples/CCI_SCGSR_SULI_VFP_2015-2021_HEPOnly_Strict.png "HEP pipeline programs 2015-2021")

## Dependencies

Required dependencies:
  - `Python 3`
  - [`pdfplumber`](https://pypi.org/project/pdfplumber/) ([GitHub](https://github.com/jsvine/pdfplumber)): Used to extract text and tables from PDFs.
    - Can be installed using the command `pip3 install --no-cache-dir pdfplumber`
    - This program has several of its own optional dependencies. More information can be found [here](https://github.com/jsvine/pdfplumber#visual-debugging).
      - [`ImageMagick`](https://www.imagemagick.org/): [Installation instructions](http://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-debian)
      - [`ghostscript`](https://www.ghostscript.com/)): [Installation instructions](https://www.ghostscript.com/doc/9.21/Install.htm)
      - **For MAC users**: Optionally by programs can be installed using the command `brew install freetype imagemagick ghostscript`
  - [`jsons`](https://pypi.org/project/jsons/) ([GitHub](https://github.com/ramonhagenaars/jsons)): Used to serialize and deserialize the class objects.
    - Can be installed using the command `pip3 install --no-cache-dir jsons`
  - [`magiconfig`](https://pypi.org/project/magiconfig/) ([GitHub](https://github.com/kpedro88/magiconfig/)): Used to read Python configuration files.
    - Can be installed using the command `pip3 install --no-cache-dir magiconfig`
  - [`matplotlib`](https://matplotlib.org/) ([PyPI](https://pypi.org/project/matplotlib/)): Used for plotting the scraped data.
    - Installation instructions can be found [here](https://matplotlib.org/stable/users/installing/index.html).
    - **TLDR**: Install using the command`pip3 install --no-cache-dir matplotlib`
  - `mpl_toolkits`: Should be installed when you install `matplotlib`. In other words, you shouldn't need to do anything extra.
  - [`GeoPandas`](https://geopandas.org/en/stable/index.html) ([PyPI](https://pypi.org/project/geopandas/)): This library is used to parse geographic data and to visualize it using `matplotlib`.
    - Installation instructions can be found [here](https://geopandas.org/en/stable/getting_started/install.html#installing-with-pip).
    - **TLDR**: You can install it using the command `pip3 install --no-cache-dir numpy pandas shapely fiona pyproj rtree GeoAlchemy2 geopy mapclassify matplotlib geopandas`

There is a script available to make sure all of the needed dependencies are installed:
```bash
python3 python/check_for_dependencies.py
```

Optional dependencies:
  - [`ShellCheck`](https://www.shellcheck.net/) ([GitHub](https://github.com/koalaman/shellcheck)): Used for linting shell scripts.
  - [`PyLint`](https://pylint.org/) ([GitHub](https://github.com/PyCQA/pylint), [PyPI](https://pypi.org/project/pylint/)): Used for linting Python modules.
  - [`bats`](https://bats-core.readthedocs.io/en/stable/) ([GitHub](https://github.com/bats-core/bats-core)): Used for unit testing shell scripts.
  - [`pytest`](https://docs.pytest.org/en/stable/) ([GitHub](https://github.com/pytest-dev/pytest/), [PyPI](https://pypi.org/project/pytest/)): Used for unit testing Python modules.

## Contributing

Pull requests are welcome, but please submit a proposal issue first, as the library is in active development.

Current maintainers:

  - Alexx Perloff

### Unit Testing

Unit testing is performed using [`bats`](https://github.com/bats-core/bats-core) for shell scripts and [`PyTest`](https://docs.pytest.org/en/stable/) for the Python modules. You are of course allowed to install these programs locally. However, shell scripts have been setup to make this procedure as easy as possible.

#### Bats for Bash scripts

The [Bats](https://bats-core.readthedocs.io/en/stable/) tests are currently setup to test the `data/download.sh` and `data/clean.sh` shell scripts. These tests rely on a stable internet connection and the government servers being healthy.

First, the Bats software needs to be setup. This is a process that only needs to happen once. To setup the software run the following command from within the repository's base directory:

```bash
test/bats_control.sh -s
```

Once the software is setup, you can run the tests using:

```bash
./test/bats_control.sh
```

If everything is working correctly, the output will be:

```bash
 ✓ Check download
 ✓ Check clean

2 tests, 0 failures
```

To remove the Bats software run:

```bash
./test/bats_control.sh -r
```

#### Pytest for Python modules

To run the python unit/integration tests, you will need to have PyTest installed. To create a local virtual environment with PyTest installed, use the following commands from within the repository's base directory:

```bash
./test/pytest_control.sh -s
```

You only have to run that command when setting up the virtual environment the first time. You can then run the tests by using the command:

```bash
./test/pytest_control.sh
```

You should see an output similar to:

```bash
======================================================== test session starts ========================================================
platform darwin -- Python 3.9.10, pytest-7.0.1, pluggy-1.0.0
rootdir: <path to WDTSscraper>
collected 2 items

test/test.py ..                                                                                                               [100%]

======================================================== 2 passed in 13.34s =========================================================
```

You can pass addition options to PyTest using the -o flag. For example, you could run the following command to increase the verbosity of PyTest:

```bash
./test/pytest_control.sh -o '--verbosity=3'
```

Other helpful pytest options include:

  - `-rP`: To see the output of successful tests. This is necessary because by default all of the output from the various tests is captured by PyTest.
  - `-rx`: To see the output of failed tests (default).
  - `-k <testname>`: Will limit the tests run to just the test(s) specified. The `<testname>` can be a class of tests or the name of a specific unit test function.

To remove the virtual environment use the command:

```bash
./test/pytest_control.sh -r
```

which will simply remove the `test/venv` directory.


### Linting

Linting is done using [`ShellCheck`](https://www.shellcheck.net/) for the Bash scripts and [`PyLint`](https://pylint.org/) for the Python code. The continuous integration jobs on GitHub will run these linters as part of the PR validation process. You may as well run them in advance in order to shorten the code review cycle. PyLint can be run as part of the Python unit testing process using the command:

```bash
test/pytest_control.sh -l
```

Unfortunately, ShellCheck is not installable via PyPI. If you install ShellCheck locally, you would need to run it using the command:

```bash
find ./ -type f -regex '.*.sh$' -not -path './/test/venv/*' -exec shellcheck -s bash -e SC2162 -e SC2016 -e SC2126 {} +
```

ShellCheck is also installed inside the Docker image and you can run it as part of method (3) from the [Using Docker](#using-docker) section. In that case you would need to run:

```bash
docker run --rm -t --mount type=bind,source=${PWD},target=/WDTSscraper aperloff/wdtsscraper:latest /bin/bash -c "find ./ -type f -regex '.*.sh$' -not -path './/test/venv/*' -exec shellcheck -s bash -e SC2162 -e SC2016 -e SC2126 {} +"
```

## Acknowledgments / Contributors

Many thanks to the following users who've contributed ideas, features, and fixes:

  - Michael Cook
  - Adam Lyon
  - Kevin Pedro