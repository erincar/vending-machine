#!/bin/sh -ex

API_DIRECTORY="`dirname $0`"/../api

# poetry run mypy $API_DIRECTORY
poetry run black \
    --preview --line-length=79 \
    --include='\.pyi?$' \
    --exclude="""\.git |
            \.__pycache__|
            \.hg|
            \.mypy_cache|
            \.tox|
            \.venv|
            _build|
            buck-out|
            build|
            dist""" \
    $API_DIRECTORY
poetry run isort --profile=black --profile=django $API_DIRECTORY
poetry run autoflake \
    --remove-all-unused-imports --recursive --remove-unused-variables \
    --in-place $API_DIRECTORY --exclude=__init__.py
poetry run flake8 \
    --max-line-length 79 --extend-ignore=E203 \
    $API_DIRECTORY