#!/bin/bash

pip install coverage==7.4.4 > /dev/null

outfile=reports/coverage/coverage.xml
while getopts o: flag
do
    case "${flag}" in
        o) outfile=${OPTARG};;
    esac
done

coverage xml $@
sed -i "" "s/timestamp=\"[0-9]*\"//g" $outfile

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