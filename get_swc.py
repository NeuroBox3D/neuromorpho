#!/usr/bin/env python
from neuromorpho import *
import argparse
from geometry_tools import check_cylinder_intersections

parser = argparse.ArgumentParser(description="Access NeuroMorpho.org v7 w/ REST API and download SWC files")
parser.add_argument('--region', required=False, type=str, help="Brain region", metavar="R")
parser.add_argument('--neurons', required=False, type=int, help="Count of neurons (-1 means all)", metavar="C")
parser.add_argument('--name', required=False, type=str, help="Name of neuron", metavar="N")
parser.add_argument('--index', required=False, type=int, help="Index of neuron", metavar="I")
parser.add_argument('--archive', required=False, type=str, help="Archive name", metavar="A")
parser.add_argument('--filters', required=False, type=str, help="One or multuple filters", metavar="[FILTER]", action='append', nargs=1)
parser.add_argument('--search', required=False, type=str, help="Search term", metavar="S")
parser.add_argument('--validate', action='store_true', help="Check for cylinder intersections")

args = parser.parse_args()

if (args.region):
  numNeurons = (args.neurons != -1 and args.neurons) or -1
  brainRegion = (args.region != -1 and args.region) or "neocortex"
  get_swc_by_brain_region(brainRegion, numNeurons)
elif (args.archive):
  numNeurons = (args.neurons != -1 and args.neurons) or -1
  archiveName = (args.archive != -1 and args.archive) or "Smith"
  get_swc_by_archive_name(archiveName, numNeurons)
elif (args.search):
    if args.index:
       fileName = get_swc_by_filter_rule_for_search_term(args.filters, args.search, 500, args.index)
       print(fileName);
       if args.validate:
          print(check_cylinder_intersections(fileName))
    else:
       fileName = get_swc_by_filter_rule_for_search_term(args.filters, args.search, args.neurons, -1)
       print(fileName)
       if args.validate:
          print(check_cylinder_intersections(fileName))
elif (not args.region and ((args.index != None) ^ (args.name != None))):
  if (args.index):
      get_swc_by_neuron_index(args.index)
  if (args.name):
      fileName = get_swc_by_neuron_name(args.name)
      if args.validate: check_cylinder_intersections(fileName)
else:
  parser.print_help()
