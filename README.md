# Neuromorpho.org API
Making use of the REST API (NeuroMorpho.org v7) to query the database for neurons and download these as files in the SWC format.
Note that the files are downloaded to your current working directory: `pwd`.

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

## CI and license
- OSX/Linux (Python v3.4/v2.7) [![OSX/Linux](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho)
- Windows (Python v2.7 and v3.4) [![Windows](https://ci.appveyor.com/api/projects/status/j0t1orah829j2yca?svg=true)](https://ci.appveyor.com/project/stephanmg/neuromorpho)
- License [![License: LGPL v3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)

