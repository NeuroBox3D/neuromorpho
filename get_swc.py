#!/usr/bin/env python
from neuromorpho import *
import argparse

parser = argparse.ArgumentParser(description="Access NeuroMorpho.org v7 w/ REST API and download SWC files")
parser.add_argument('--region', required=False, type=str, help="Brain region", metavar="R")
parser.add_argument('--neurons', required=False, type=int, help="Count of neurons (-1 means all)", metavar="C")
parser.add_argument('--name', required=False, type=str, help="Name of neuron", metavar="N")
parser.add_argument('--index', required=False, type=int, help="Index of neuron", metavar="I")
parser.add_argument('--archive', required=False, type=str, help="Archive name", metavar="A")
args = parser.parse_args()

if (args.region):
  numNeurons = (args.neurons != -1 and args.neurons) or -1
  brainRegion = (args.region != -1 and args.region) or "neocortex"
  get_swc_by_brain_region(brainRegion, numNeurons)
elif (args.archive):
  numNeurons = (args.neurons != -1 and args.neurons) or -1
  archiveName = (args.archive != -1 and args.archive) or "Smith"
  get_swc_by_archive_name(archiveName, numNeurons)
elif (not args.region and ((args.index != None) ^ (args.name != None))):
  if (args.index):
      get_swc_by_neuron_index(args.index)
  if (args.name):
      get_swc_by_neuron_name(args.name)
else:
  parser.print_help()
