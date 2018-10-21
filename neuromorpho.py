""" Making use of the  REST API (NeuroMorpho.org v7) to query the database """

try:
  from urllib2 import urlopen
  from urllib2 import Request
except ImportError:
  from urllib.request import urlopen
  from urllib.request import Request

import re
import json
import base64

# "constant" URL to the database
NEUROMORPHO_URL = "http://neuromorpho.org"

def check_api_health():
  """ Checks if the REST API is available """
  url = "http://neuromorpho.org/api/health"
  req = Request(url)
  response = urlopen(req)
  if (json.loads(response.read())['status'].decode('utf-8') != "UP"):
      print("REST API not available")
      return False
  return True

def get_swc_by_neuron_index(neuronIndex):
  """Download a neuron by index and store it into a SWC file

    Keyword arguments:
    neronIndex -- the neuron index in the database
  """
  if (not check_api_health()): return
  url = "%s/api/neuron/id/%i" % (NEUROMORPHO_URL, neuronIndex)
  req = Request(url)
  response = urlopen(req)
  neuronName = json.loads(response.read().decode('utf-8'))['neuron_name']
  url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuronName)
  html = urlopen(url).read()
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
     open(fileName, 'w').write(response.read())

def get_swc_by_neuron_name(neuronName):
  """ Download the SWC file specified by the neuron's name """
  if (not check_api_health()): return
  pass

def get_all_swcs_by_region(regionName):
  """ Download all SWCs specified by a region name """
  # http://neuromorpho.org/api//neuron/select?q=brain_region:neocortex&size=500&page=1
  if (not check_api_health()): return
  pass
