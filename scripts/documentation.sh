#!/bin/bash

pip install pdoc3

pdoc --html --output-dir temp rest_wrapper
mv rest_wrapper docs

