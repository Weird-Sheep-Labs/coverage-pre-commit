#!/bin/bash

# pre-commit doesn't hook into user's venv so need to install required packages 
pip install coverage==7.4.4 > /dev/null

# Specify default output file location but replace with user-specified override if present
outfile=reports/coverage/coverage.xml
while getopts o: flag
do
    case "${flag}" in
        o) outfile=${OPTARG};;
    esac
done

# Override default output file location and generate coverage report
coverage xml $@ -o $outfile

# Remove timestamp from output file to avoid unnecessary diffs
sed -i "" "s/timestamp=\"[0-9]*\"//g" $outfile

# Exits non-zero if generated file is modified or untracked (initial creation)
if git status -s | awk '/[AM ]M / { print $2 }' | 
    grep --quiet --fixed-strings $outfile 
then    
    exit 1
else
    if git ls-files --others --exclude-standard | 
        grep --quiet --fixed-strings $outfile
    then
        exit 1
    else
        exit 0
    fi
fi