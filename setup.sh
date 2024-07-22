#!/usr/bin/env bash

# Ensure a Python environment
[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
python --version

pip install -U -r requirements.txt
