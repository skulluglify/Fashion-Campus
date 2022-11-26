#!/usr/bin/env bash

cd $(dirname $0)

export PYTHONPATH=api
export IMAGE_FOLDER=`pwd`/images

python3 api/main.py