#!/usr/bin/env bash
##
## Copyright (c) 2022 by Dribia Data Research.
## This file is part of project Bowser,
## and is released under the MIT License Agreement.
## See the LICENSE file for more information.
##

set -e  # Run linting only until the first error.
set -x  # Print commands.

# This script runs all the necessary linting processes
# to make sure the code follows the style guides and does
# not have type hint errors.

# Execute all the linting checks
poetry run black product_rater tests scripts --check
poetry run ruff product_rater tests scripts
poetry run mypy product_rater
