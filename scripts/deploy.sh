#!/bin/bash

pip install wheel

python setup.py sdist bdist_wheel

zip -r "my-artifact.zip" dist/
