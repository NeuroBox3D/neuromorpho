""" Making use of the  REST API (NeuroMorpho.org v7) to query the database """
import urllib2
import re
import json
import base64

# "constant" URL to the database
NEUROMORPHO_URL = "http://neuromorpho.org"

def check_api_health():
  """ Checks if the REST API is available """
  url = "http://neuromorpho.org/api/health"
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  if (json.loads(response.read())['status'] != "UP"):
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
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  neuronName = json.loads(response.read())['neuron_name']
  url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuronName)
  html = urllib2.urlopen(url).read()
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urllib2.urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
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
