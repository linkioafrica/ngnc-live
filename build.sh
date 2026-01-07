#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip to the latest version
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input
