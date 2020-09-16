# Python Wrapper for the NeuroMorpho.org website

The NeuroMorpho.org database is centrally curated inventory of reconstructions of neurons which are associated with peer-reviewed publications. 
The provided Python wrapper makes the interaction with the website through the NeuroMorpho.org v7 REST API available for procedural processing, 
e.g. batch processing. The database can be queried, and neurons can be downloaded in the SWC file format. See `get_swc.py` or the examples below.
Additionally consistency of the geometry can be checked with the `--validate` switch. This checks for self-intersections of the cylinders.

This Python wrapper depends only on the Python 2/3 standard libraries, so no additional dependencies are required to run it.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7934336da8264b259928f04288102a17)](https://app.codacy.com/gh/NeuroBox3D/neuromorpho?utm_source=github.com&utm_medium=referral&utm_content=NeuroBox3D/neuromorpho&utm_campaign=Badge_Grade_Dashboard)
 [![OSX/Linux](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho)
[![Windows](https://ci.appveyor.com/api/projects/status/j0t1orah829j2yca?svg=true)](https://ci.appveyor.com/project/stephanmg/neuromorpho)
[![License: MIT](https://img.shields.io/badge/License-MIT-magenta.svg)](https://opensource.org/licenses/MIT)
 [![PyPI version](https://badge.fury.io/py/neuromorpho.svg)](https://badge.fury.io/py/neuromorpho)

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
