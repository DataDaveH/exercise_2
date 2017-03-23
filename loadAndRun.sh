#!/bin/bash

# make absolute path directory where the spouts and bolts can get at their dependencies
mkdir ~/ex2Files

cp ./config.ini ~/ex2Files
cp ./myDBObj.py ~/ex2Files
touch ~/ex2Files/__init__.py

MY_CWD=$(pwd)

# see if command line param specified for tracking
if [[ $# -eq 1 ]]
    sed 's/\(^track\s*=\)\(.*\)/\1 '$1'/' config.ini

cd extweetcount

# run the topology
sparse run

cd $MY_CWD

exit
