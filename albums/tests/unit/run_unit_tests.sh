#!/bin/bash

export ENV='test'

printf "Running unit tests for Users\n"
python3 -m unittest albums/tests/unit/test_users.py

printf "Running unit tests for Albums\n"
python3 -m unittest albums/tests/unit/test_albums.py