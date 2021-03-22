#!/bin/bash

pip install pdoc3

mkdir docs
pdoc --html --output-dir docs rest_wrapper
