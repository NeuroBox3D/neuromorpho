# Neuromorpho
Making use of the  REST API (NeuroMorpho.org v7) to query the database.

## Features
- Get SWC file by neuron ID
- Get SWC file by neuron name
- Get SWC file by brain region

## Usage:
- `python get_swc.py` will output some help method
- `python get_swc.py --region neocortex` will download all swc to current dir
- `python get_swc.py --region neocortex --neurons 10` will download the first 10 neurons
- `python get_swc.py --name cnic_001` will download the specified neuron by name
- `python get_swc.py --index 1` will download the specified neuron by index

Note region cannot specified with name or index, and either name or index can be specified.

## CI
- OSX/Linux (Python v3.4/v2.7) [![OSX/Linux](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho)
- Windows (Python v2.7 and v3.4) [![Windows](https://ci.appveyor.com/api/projects/status/j0t1orah829j2yca?svg=true)](https://ci.appveyor.com/project/stephanmg/neuromorpho)
