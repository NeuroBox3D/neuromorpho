#!/bin/bash

pip install pdoc3

mkdir docs
pdoc --html rest_wrapper
