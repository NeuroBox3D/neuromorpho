# Python module for accessing NeuroMorpho.org 

The *NeuroMorpho.org* database is centrally curated inventory of reconstructions of neurons which are associated with peer-reviewed publications. 
The provided Python wrapper makes the interaction with the website through the NeuroMorpho.org v7 REST API available for procedural processing, 
e.g. batch processing. The database can be queried, and neurons can be downloaded in the SWC file format. See `get_swc.py` or the examples below.
Additionally consistency of the geometry can be checked with the `--validate` switch. This checks for self-intersections of the cylindrical geometry 
in three-dimensional space. 

Depends only on standard modules, no 3rd party dependencies. **Python >=2.5** is required however.

A first example can be found [here](https://gist.github.com/stephanmg/1bed6eba540a3710da5d60888d0c701a) and the API documentation [there](https://neurobox3d.github.io/neuromorpho/).

### Build status

| Linux  | Windows | OSX |
|---|---|---|
|  [![Linux](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho) | [![Windows](https://ci.appveyor.com/api/projects/status/j0t1orah829j2yca?svg=true)](https://ci.appveyor.com/project/stephanmg/neuromorpho) |  [![OSX](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho) |

[![Docs](https://img.shields.io/badge/Pydoc-%20Documentation-blueviolet.svg)](https://neurobox3d.github.io/neuromorpho/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7934336da8264b259928f04288102a17)](https://app.codacy.com/gh/NeuroBox3D/neuromorpho?utm_source=github.com&utm_medium=referral&utm_content=NeuroBox3D/neuromorpho&utm_campaign=Badge_Grade_Dashboard)
[![CodeQL](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/codeql-analysis.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-magenta.svg)](https://opensource.org/licenses/MIT)
 [![PyPI version](https://badge.fury.io/py/neuromorpho.svg)](https://badge.fury.io/py/neuromorpho)
 [![Python >=2.6](https://img.shields.io/badge/python-2.5-blue.svg)](https://www.python.org/downloads/release/python-250/)
 [![Build](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/build.yml/badge.svg)](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/build.yml)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/NeuroBox3D/neuromorpho)
[![GitHub issues open](https://img.shields.io/github/issues/NeuroBox3D/neuromorpho)](https://github.com/NeuroBox3D/neuromorpho/issues)
[![Documentation](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/documentation.yml/badge.svg)](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/documentation.yml)
[![Build](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/build.yml/badge.svg)](https://github.com/NeuroBox3D/neuromorpho/actions/workflows/build.yml) [![Join the chat at https://gitter.im/NeuroBox3D/neuromorpho](https://badges.gitter.im/NeuroBox3D/neuromorpho.svg)](https://gitter.im/NeuroBox3D/neuromorpho?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## Features
- Get neurons matching a search term and additional filters (Usage Example 1 and 2)
- Get a neuron by global index in database (Example 3)
- Get a neuron by known name in database (Example 4)
- Get a certain number of neurons by brain region (Example 5)
- Get a certain number of neurons by archive name (Example 6)

## Usage:

### Example 0

Omitting any arguments and just typing `python get_SWC.py` in a a terminal will output the following usage string:
```
usage: get_swc.py [-h] [--region R] [--neurons C] [--name N] [--index I]
                  [--archive A] [--filters [FILTER]] [--search S]

Access NeuroMorpho.org v7 w/ REST API and download SWC files

optional arguments:
  -h, --help          show this help message and exit
  --region R          Brain region
  --neurons C         Count of neurons (-1 means all)
  --name N            Name of neuron
  --index I           Index of neuron
  --archive A         Archive name
  --filters [FILTER]  One or multiple filters (OPTIONAL)
  --search S          Search term
  ```

### Example 1

Most useful usage is probably the following to specify a search term and additional filters:

`python get_swc.py --filter "cell_type=pyramidal" --neurons 10 --search "brain_region:neocortex" --filter "archive=Allen Cell Types"`

This will search for the brain region *neocortex* and then filter the result by the *cell type* pyramidal and *archive* Allen Cell Types.
The first 10 neurons stored in *NeuroMorpho.org* database will then be downloaded and stored as **SWC** files.

### Example 2

Get a neuron of this search term by index of total neurons matching the search criteria (The below will pick neuron with index 7):

`python get_swc.py --filter "cell_type=pyramidal" --index 7 --search "brain_region:neocortex" --filter "archive=Allen Cell Types"`

### Example 3

Get a neuron (Here: The first neuron in the database) by the global index (1) from the database:
- `python get_SWC.py --index 1`

### Example 4

Get a neuron by it's known name and download as SWC file:
- `python get_SWC.py --name cnic_001`

### Example 5

The following will download *all* SWC files from the region *Neocortex* to the current working directory
- `python get_SWC.py --region neocortex`

and the following command will just download the first ten neurons from the *Neocortex* region.
- `python get_SWC.py --region neocortex --neurons 10`

### Example 6

To download a whole *Smith* archive in SWC format from the database, use the following commmand:
- `python get_SWC.py --archive Smith` 
