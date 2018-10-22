""" Making use of the REST API (NeuroMorpho.org v7) to query the database """
# python v2 or v3
try:
  from urllib2 import urlopen, Request
except ImportError:
  from urllib.request import urlopen, Request

import re
import json
import base64

# "constants"
NEUROMORPHO_URL = "http://neuromorpho.org"
MAX_NEURONS_PER_PAGE = 500

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
  neuronName = json.loads(response.read().decode("utf-8"))['neuron_name']
  url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuronName)
  html = urlopen(url).read()
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
     open(fileName, 'w').write(response.read())

def get_swc_by_neuron_name(neuronName):
  """ Download the SWC file specified by the neuron's name

    Keyword arguments:
    neuronIndex -- the neuron index in the database
  """
  if (not check_api_health()): return
  url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuronName)
  html = urlopen(url).read()
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
     open(fileName, 'w').write(response.read())

def get_swc_by_brain_region(brainRegion, neuronPages=-1, neuronsPerPage=-1):
  """ Download all SWCs specified by a region name

    Keyword arguments:
    brainRegion -- the brain region
    neuronPages -- how many pages of the neurons we want (-1 means all pages)
    neuronsPerPage -- how many neurons per page (-1 means maximum per page)
  """
  if (not check_api_health()): return
  numNeurons = (neuronsPerPage != -1 and neuronsPerPage < MAX_NEURONS_PER_PAGE) and neuronsPerPage
  url = "%s/api/neuron/select?q=brain_region:%s&size=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons)
  req = Request(url)
  response = urlopen(req)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = (neuronPages != -1 and neuronPages < totalPages) and neuronPages
  for page in xrange(0, numNeuronPages):
    url = "%s/api/neuron/select?q=brain_region:%s&size=%i&page=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    for neuron in xrange(0, numNeurons):
      get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])
