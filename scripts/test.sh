#!/usr/bin/env bash
##
## Copyright (c) 2022 by Dribia Data Research.
## This file is part of project Bowser,
## and is released under the MIT License Agreement.
## See the LICENSE file for more information.
##

set -e
set -x

poetry run sh ./scripts/lint.sh
poetry run pytest --cov=product_rater --cov=tests --cov-report=html tests "$@"
