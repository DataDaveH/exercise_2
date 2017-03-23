#!/bin/bash

# make absolute path directory where the spouts and bolts can get at their dependencies
LOAD_DIR=~/ex2Files
mkdir -p $LOAD_DIR

cp ./config.ini ~/ex2Files
cp ./myDBObj.py ~/ex2Files
touch ~/ex2Files/__init__.py

# see if command line param specified for tracking
if [[ $# -eq 1 ]]; then
    # update the ini file with the new key before copying
    sed -i 's/\(^track\s*=\)\(.*\)/\1 '$1'/' $LOAD_DIR/config.ini
fi

MY_CWD=$(pwd)
cd ./extweetwordcount

# run the topology
sparse run

cd $MY_CWD

# empty and remove dependency dir
rm ~/ex2Files/*
rmdir ~/ex2Files

exit
