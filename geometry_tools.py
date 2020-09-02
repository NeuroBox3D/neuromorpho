#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from read_swc import read_swc
sys.path.insert(0, "externals")
from csg.core import CSG
from itertools import combinations

def check_cylinder_intersections(fileName):
  """ Check if cylinder-cylinder intersections occur with CSG tools (BSP trees)
  
  Keyword arguments:
  fileName -- the name of the file which should be checked for intersections
  """
  edges = read_swc(fileName)

  for combination in combinations(range(0, len(edges), 2), 2):
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

    # check for intersections
    a = CSG.cylinder(radius=0.5*(d1+d2), start=p1, end=p2, slices=16)
    b = CSG.cylinder(radius=0.5*(d3+d4), start=p3, end=p4, slices=16)
    polys = a.intersect(b)

    if polys.toPolygons():
      print(polys.toPolygons())
      print("Cylinders intersect in neuron with name %s" % fileName)
      print("Cylinders: A (%f;%s;%s) and B(%f;%s;%s)" %(0.5*(d1+d2), p1, p2, 0.5*(d3+d4), p3, p4))
      return

  return False


def read_swc(fileName):
    """ Read in a SWC file from Neuromorpho
  
     Keywords arguments:
     fileName -- the file name corresponding to the SWC to be read
    """
    edges = []
    points = []
    line = ""
    lineCnt = 0
    curInd = 0
    indexMap = {}
    diams = []
    types = []
    if not os.path.isfile(fileName):
       print("File path {} does not exist. Exiting...".format(fileName))
       sys.exit()
    
    with open(fileName, "r") as f:
      line = f.readline()
      lineCnt = lineCnt + 1
      line = line.rstrip().lstrip()
      
      while line:
        line = f.readline()
        # ignore empty lines
        if len(line) == 0: continue
        # ignore comments
        if line.startswith("#"): continue
        # split
        splitted = line.split()
        if not len(splitted) == 7:
          print("Line {} does not contain 6 columns...".format("\t".join(splitted)))
        
        indexMap[int(splitted[0])] = curInd
        points.append([float(splitted[2]), float(splitted[3]), float(splitted[4])])
        diams.append(float(splitted[5]))
        types.append(int(splitted[0]))
        # 2, 3, 4 are x, y, z coordinates
        # 6 is connection
        conn = int(splitted[6])
        if conn >= 0:
          parentID = indexMap[conn]
          parent = points[parentID]
          diameter = diams[parentID]
          t = types[parentID]
          edges.append([points[conn], parent, diameter, t])
        curInd = curInd + 1
    return edges
