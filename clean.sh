#!/usr/bin/env bash

for i in $(find . -type d | grep -Ei '(\.mypy_cache|__pycache__)$'); do echo $i; rm -rf $i; done
