#!/bin/bash

pip install genbadge[coverage] > /dev/null

outfile=coverage-badge.svg
while getopts o: flag
do
    case "${flag}" in
        o) outfile=${OPTARG};;
    esac
done

genbadge coverage $@
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