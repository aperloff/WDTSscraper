#!/usr/bin/env bats

setup() {
	load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'

    # get the containing directory of this file
    # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
    # as those will point to the bats executable's location or the preprocessed file respectively
    DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
    # make executables in src/ visible to PATH
    PATH="$DIR/..:$PATH"
}

@test "Check download" {
    run data/download.sh
    refute_output --partial 'MISSING'
    assert_output --partial 'SUCCESS::'
}

@test "Check clean" {
	run data/clean.sh
	refute_output --partial 'ERROR::'
	assert_output --partial 'SUCCESS::'
}
