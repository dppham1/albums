#!/bin/bash

export ENV='test'

printf "Running integration tests for Users\n"
python3 -m unittest albums/tests/integration/test_users.py

printf "Running integration tests for Albums\n"
python3 -m unittest albums/tests/integration/test_albums.py