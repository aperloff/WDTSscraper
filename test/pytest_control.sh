#!/bin/bash

error_pytest_control() {
    echo -e "ERROR: $*. Aborting." >&2
    return 1
}

setup_pytest_venv() {
    python3 -m venv test/venv
    if [[ -f "test/venv/bin/activate" ]]; then
        echo "Starting the virtual environment now ..."
        # shellcheck disable=SC1091
        source test/venv/bin/activate
        pip install --no-cache-dir -r requirements.txt
    else
        error_pytest_control "The directory '${PWD}/test/venv' does not exist. Cannot enter the virtual environment"
    fi
}

run_lint() {
    if [[ -f "test/venv/bin/activate" ]] && [[ "$VIRTUAL_ENV" == "" ]]; then
        # shellcheck disable=SC1091
        source test/venv/bin/activate
    fi

    if [[ "$VIRTUAL_ENV" != "" ]]; then
        find ./ -type f -regex '.*.py$' -not -path './/test/venv/*' -exec pylint {} +
    else
        error_pytest_control "Unable to start the virtual environment containing pytest." \
                             "Make sure you have run './test/pytest_control.sh -s'"
    fi
}

run_pytest() {
    if [[ -f "test/venv/bin/activate" ]] && [[ "$VIRTUAL_ENV" == "" ]]; then
        # shellcheck disable=SC1091
        source test/venv/bin/activate
    fi

    if [[ "$VIRTUAL_ENV" != "" ]]; then
        if [[ -f "test/test.py" ]]; then
            IFS=' '; read -r -a OPTIONS_ARRAY <<<"${1}"
            pytest test/test.py -W ignore::DeprecationWarning "${OPTIONS_ARRAY[@]}"
        else
            error_pytest_control "Unable to locate the files containing the tests to run ('test/test.py')." \
                                 "Make sure the virtual environment was setup from within the WDTSscraper directory"
        fi
    else
        error_pytest_control "Unable to start the virtual environment containing pytest." \
                             "Make sure you have run './test/pytest_control.sh -s'"
    fi
}

teardown_pytest_venv() {
    if [[ -d "test/venv" ]]; then
        rm -rf test/venv
    else
        error_pytest_control "The directory '${PWD}/test/venv' does not exist. Cannot remove the virtual environment"
    fi
}

usage() {
cat <<EOF
usage: pytest_control.sh [options]

This script sets up or tears down (removes) the software needed to run the pytest unit/integration tests
on the python modules in aperloff/WDTSscraper.

OPTIONS:
    -o      Run with additional pytest options
    -r      Remove the virtual environment
    -s      Setup the virtual environment
EOF
}

OPTIND=1
LINT="False"
OPTIONS=""
REMOVE="False"
SETUP="False"

#check arguments
while getopts "hlo:rs" option; do
    case "${option}" in
        l)  LINT="True"
            ;;
        o)  OPTIONS=${OPTARG}
            ;;
        r)  [[ "${SETUP}" == "True" ]] && error_pytest_control "Cannot specify option -r after specifying option -s"
            REMOVE="True"
            ;;
        s)  [[ "${REMOVE}" == "True" ]] && error_pytest_control "Cannot specify option -s after specifying option -r"
            SETUP="True"
            ;;
        h)  usage
            exit 2
            ;;
        \?) echo "Invalid option: -$OPTARG" >&2
            usage
            exit 3
            ;;
        :)  echo "Option -$OPTARG requires an argument." >&2
            exit 4
            ;;
    esac
done

if [[ "${SETUP}" == "True" ]]; then
    setup_pytest_venv
elif [[ "${REMOVE}" == "True" ]]; then
    teardown_pytest_venv
elif [[ "${LINT}" == "True" ]]; then
    run_lint
else
    run_pytest "${OPTIONS}"
fi
