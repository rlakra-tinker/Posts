#!/bin/bash
# Author: Rohtash Lakra
echo
if [ "$1" == "production" ]; then
  python -m unittest discover -s ./tests -p "test_*.py"
else
  python3 -m unittest
fi
echo
