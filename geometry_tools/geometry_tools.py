#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, "externals")
from csg.core import CSG
from itertools import combinations
from collections import namedtuple

def read_swc_to_edge_list(filename):
    """Read in a SWC file from Neuromorpho
     Keywords arguments:
     filename -- the file name corresponding to the SWC to be read
    """
    if not os.path.isfile(filename):
       print("File path {} does not exist. Exiting...".format(filename))
       sys.exit(1)

    SWCPoint = namedtuple("SWCPoint", "index compartment x y z diam pid")
    points = []
    with open(filename, "r") as f:
      line = f.readline()
      line = line.rstrip().lstrip()

      while line:
        line = f.readline()
        # ignore empty lines
        if len(line) == 0: continue

        # ignore comments
        if line.startswith("#"): continue

        # split the current line
        splitted = line.split()
        if not len(splitted) == 7:
          print("Line {} does not contain 6 columns...".format("\t".join(splitted)))
        else:
          points.append(SWCPoint(*splitted))

    edges = []
    for p in points:
      # parent id
      pid = int(p.pid) - 1
      # root has no parent
      if pid == -1: continue
      # points list start at index 0, SWC starts at index 1, thus subtract 1 from pid
      parent = points[pid-1]
      # one edge whhich will be used to define a cylinder
      edges.append([[float(p.x), float(p.y), float(p.z)], [float(parent.x), float(parent.y),
                    float(parent.z)], float(parent.diam), int(parent.compartment)])
    return edges


def check_cylinder_intersections(filename):
  """Check if cylinder-cylinder intersections occur with CSG tools (BSP trees)
  
  Keyword arguments:
  filename -- the name of the file which should be checked for intersections
  """
  edges = read_swc_to_edge_list(filename)

  numIntersections = 0

  for combination in combinations(range(0, len(edges)-2, 2), 2):
    p1 = edges[combination[0]+0][0]
    p2 = edges[combination[0]+1][1]
    d1 = edges[combination[0]+0][2]
    d2 = edges[combination[0]+1][2]

    p3 = edges[combination[1]+0][0]
    p4 = edges[combination[1]+1][1]
    d3 = edges[combination[1]+0][2]
    d4 = edges[combination[1]+1][2]
  
    t1 = edges[combination[0]+0][3]
    t2 = edges[combination[0]+1][3]
    t3 = edges[combination[1]+0][3]
    t4 = edges[combination[1]+1][3]

    # ignore soma cylinders (as they are error-prone)
    if (t1 == 1 or t2 == 1 or t3 == 1 or t4 == 1): continue

    # ignore self-loops (should actually never happen)
    if (p1 == p2 or p3 == p4): continue
    # ignore adjacent cylinders
    if (p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4): continue

    # check for intersections
    a = CSG.cylinder(radius=0.5*(d1+d2), start=p1, end=p2, slices=4)
    b = CSG.cylinder(radius=0.5*(d3+d4), start=p3, end=p4, slices=4)
    polys = a.intersect(b)

    if polys.toPolygons():
      print(polys.toPolygons())
      print("Cylinders intersect in neuron with name %s" % filename)
      print("Cylinders: A (%f;%s;%s) and B(%f;%s;%s)" %(0.5*(d1+d2), p1, p2, 0.5*(d3+d4), p3, p4))
      numIntersections = numIntersections + 1

  return numIntersections > 0 and True or False


