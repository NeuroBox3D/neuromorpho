#!/bin/bash

python setup.py sdist bdist_wheel

zip -r "my-artifact.zip" dist/
