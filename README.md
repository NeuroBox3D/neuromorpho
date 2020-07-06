# Neuromorpho
Making use of the REST API (NeuroMorpho.org v7) to query the database.

## Features
- Get SWC file by neuron index
- Get SWC file by neuron name
- Get SWC files by brain region
- Get SWC files by archive name

## Usage:

` usage: get_swc.py [-h] [--region R] [--neurons C] [--name N] [--index I]
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
  --search S          Search term `


Most useful usage is probably the following to specify a search term and additional filters:

`python get_swc.py --filter "cell_type=pyramidal" --neurons 10 --search "brain_region:neocortex" --filter "archive=Allen Cell Types"`

This will search for the brain region *neocortex* and then filter the result by the *cell type* pyramidal and *archive* Allen Cell Types.
The first 10 neurons stored in *NeuroMorpho.org* database will then be downloaded and stored as **SWC** files.

Or: Get a neuron of this search term by index of total neurons matching the search criteria (The below will pick neuron with index 7):

`python get_swc.py --filter "cell_type=pyramidal" --index 7 --search "brain_region:neocortex" --filter "archive=Allen Cell Types"`

- `python get_SWC.py` will output some help information
- `python get_SWC.py --region neocortex` will download all SWC files from the region *neocortex* to current dir
- `python get_SWC.py --region neocortex --neurons 10` will download the first 10 SWC files of the region *neocortex* to current dir
- `python get_SWC.py --name cnic_001` will download the specified SWC file by name to current dir
- `python get_SWC.py --index 1` will download the specified SWC file by index to current dir
- `python get_SWC.py --archive Smith` will download all SWC files of given archive name *Smith* to current dir

Note that region cannot be specified with name or index, and either name or index can be specified.

## CI
- OSX/Linux (Python v3.4/v2.7) [![OSX/Linux](https://travis-ci.org/NeuroBox3D/neuromorpho.svg?branch=master)](https://travis-ci.org/NeuroBox3D/neuromorpho)
- Windows (Python v2.7 and v3.4) [![Windows](https://ci.appveyor.com/api/projects/status/j0t1orah829j2yca?svg=true)](https://ci.appveyor.com/project/stephanmg/neuromorpho)
