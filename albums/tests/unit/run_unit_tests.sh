#!/bin/bash

export ENV='test'

printf "Running unit tests for Users"
python3 -m unittest albums/tests/unit/test_users.py

printf "\n"

printf "Running unit tests for Albums"
python3 -m unittest albums/tests/unit/test_albums.py