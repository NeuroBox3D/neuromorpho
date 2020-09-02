#!/usr/bin/env python
## Read SWC file and creates directions from successive points / edges
import os, sys
import numpy as np

def create_vectors(edges):
  """ Creates vectors from edge pairs
  
  Keyword arguments:
  edges -- edges
  """
  vectors = []
  for edge in edges:
    vectors.append(np.subtract(np.array(edge[0]), np.array(edge[1])))
  return vectors

def read_swc(fileName):
    """ Read in a SWC file from Neuromorpho
  
     Keywords arguments:
     fileName -- the file
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

if __name__ == "__main__":
  edges = read_swc("30-6-2-HCB.CNG.swc")
  vectors = create_vectors(edges)
  for vector in vectors: print(vector)
