#!/bin/bash

# pre-commit doesn't hook into user's venv so need to install required packages 
pip install genbadge[coverage]==1.1.1 > /dev/null

# Specify default file locations but replace with user-specified overrides if present
infile=reports/coverage/coverage.xml
outfile=reports/coverage/coverage-badge.svg
while getopts i:o: flag
do
    case "${flag}" in
        i) infile=${OPTARG};;
        o) outfile=${OPTARG};;
    esac
done

# Check input file location is valid; raise error if not
if ! test -f $infile; then
  echo "Could not find coverage XML file: $infile"
  exit 1
fi

# Override default file locations and generate badge
genbadge coverage $@ -i $infile -o $outfile

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