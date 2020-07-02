# Neuromorpho
Making use of the REST API (NeuroMorpho.org v7) to query the database.

## Features
- Get SWC file by neuron index
- Get SWC file by neuron name
- Get SWC files by brain region
- Get SWC files by archive name

## Usage:
Most useful usage is probably the following to specify a search term and additional filters:

`python get_swc.py --filter "cell_type=pyramidal" --neurons 10 --search "brain_region:neocortex" --filter "archive=Allen Cell Types"`

This will search for the brain region *neocortex* and then filter the result by the *cell type* pyramidal and *archive* Allen Cell Types.
The first 10 neurons stored in *NeuroMorpho.org* database will then be downloaded and stored as **SWC** files.

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
