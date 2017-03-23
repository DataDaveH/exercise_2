#!/bin/bash

# see if command line param specified for tracking
if [ $# -eq 1 ]; then
    sed 's/\(^track\s*=\)\(.*\)/\1 '$1'/' config.ini
fi

exit
