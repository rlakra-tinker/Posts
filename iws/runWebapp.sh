#!/bin/bash
# Author: Rohtash Lakra
echo
if [ $# -gt 0 ]; then
  gunicorn -c webapp/gunicorn.conf.py webapp:app
else
  python -m flask --app webapp run --port 8080 --debug
fi
echo
