#!/usr/bin/env python
from neuromorpho import *
import argparse

parser = argparse.ArgumentParser(description="Access NeuroMorpho.org v7 w/ REST API")
parser.add_argument('--region', required=False, type=str, help="Brain region", metavar="R")
parser.add_argument('--neurons', required=False, type=int, help="Count of neurons per page", metavar="C")
parser.add_argument('--pages', required=False, type=int, help="Number of pages of neurons", metavar="P")
parser.add_argument('--name', required=False, type=str, help="Name of neuron", metavar="N")
parser.add_argument('--index', required=False, type=int, help="Index of neuron", metavar="I")
args = parser.parse_args()

if (args.region):
  numNeurons = (args.neurons != -1 and args.neurons) or -1
  numPages = (args.pages != -1 and args.neurons) or -1
  brainRegion = (args.region != -1 and args.region) or "neocortex"
  get_swc_by_brain_region(brainRegion, numNeurons, numPages)
if (not args.region and ((args.index != None) ^ (args.name != None))):
  if (args.index):
      get_swc_by_neuron_index(args.index)
  if (args.name):
      get_swc_by_neuron_name(args.name)
else:
  parser.print_help()
