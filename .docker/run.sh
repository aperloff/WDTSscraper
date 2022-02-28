#!/usr/bin/env bash

# This script an image inside a docker container.
# Arguments:
#  1. The arguments to WDTSscraper.py

action() {
    local this_file
    local this_dir
    local root_dir
    this_file="$( [ -n "$ZSH_VERSION" ] && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    this_dir="$( cd "$( dirname "$this_file" )" && pwd )"
    root_dir="$( dirname "$this_dir" )"

    # get the arguments
    local args="${*}"

    # define docker args and cmd depending on the arguments
    local docker_args="--rm -t --mount type=bind,source=\"${root_dir}\",target=/WDTSscraper"
    local docker_cmd=""
    if [ -n "${args}" ]; then
        docker_cmd="python3 python/WDTSscraper.py ${args}"
    else
        2>&1 echo "No arguments for WDTSscraper.py provided"
        return "1"
    fi

    # start the container
    local image="aperloff/wdtsscraper:latest"
    local cmd="docker run ${docker_args} ${image} ${docker_cmd}"
    echo -e "command: ${cmd}\n"
    eval "$cmd"
}
action "$@"