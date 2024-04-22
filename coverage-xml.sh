#!/bin/bash

pip install coverage > /dev/null

outfile=coverage.xml
while getopts o: flag
do
    case "${flag}" in
        o) outfile=${OPTARG};;
    esac
done

coverage xml $@
sed -i "" "s/timestamp=\"[0-9]*\"//g" $outfile

if ! git rev-parse --verify HEAD >/dev/null 2>&1
then
    exit 1
fi

exec 1>&2

if ! git diff --cached --name-only HEAD |
    grep --quiet --fixed-strings $outfile || 
    git ls-files --others --exclude-standard | 
    grep --quiet --fixed-strings $outfile
then    
    exit 1
else
    exit 0
fi