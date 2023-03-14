#!/bin/bash

export ENV='test'

printf "Running unit tests for Users"
nosetests  --nocapture albums/tests/unit/test_users.py 

printf "\n"

printf "Running unit tests for Albums"
nosetests albums/tests/unit/test_albums.py --nocapture