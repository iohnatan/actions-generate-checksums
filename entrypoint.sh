#!/bin/bash

python3 /action.py --pattern "$1" --checksum_extension "$2" --subfolder "$3" --paths_ignore "$4"
