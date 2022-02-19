#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

python ./manage.py db init || true  # Can fail if already set up
python ./manage.py db migrate
python ./manage.py db upgrade
python ./run.py
