""" Making use of the REST API (NeuroMorpho.org v7) to query the database """
# python v2 or v3
try:
  from urllib2 import urlopen, Request
except ImportError:
  from urllib.request import urlopen, Request

import re, json, base64, sys

# pseudo-constants
NEUROMORPHO_URL = "http://neuromorpho.org"
MAX_NEURONS_PER_PAGE = 500

def validate_response_code(response):
  """ Checks response code from JSON request and print warning then exits """
  code = response.getcode()
  # success
  if code == 200: return

  # error codes
  if code == 400:
      print "Bad request, usually wrong parameters to select queries."
  elif code == 404:
      print "Resource not found or does not exist"
  elif code == 405:
      print "Unsupported HTTP method used (No GET or POST request)."
  elif code == 500:
      print "Internal Server Error. Contact admin for assistance."

  sys.exit()

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
  validate_response_code(response)
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
    neuronName -- the neuron index in the database
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

    Note: Brain regions usually start in lowercase
  """
  if (not check_api_health()): return
  if (not brainRegion[0].islower()): print "Warning: brain region does not start with lower case letter"
  numNeurons = neuronsPerPage if (neuronsPerPage != -1 and neuronsPerPage < MAX_NEURONS_PER_PAGE) else MAX_NEURONS_PER_PAGE
  url = "%s/api/neuron/select?q=brain_region:%s&size=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons)
  req = Request(url)
  response = urlopen(req)
  validate_response_code(response)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = neuronPages if (neuronPages != -1 and neuronPages < totalPages) else totalPages
  for page in xrange(0, numNeuronPages):
    url = "%s/api/neuron/select?q=brain_region:%s&size=%i&page=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    for neuron in xrange(0, numNeurons):
      get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])

def get_swc_by_archive_name(archiveName, neuronPages=-1, neuronsPerPage=-1):
  """ Download all SWCs specified by an archive name

    Keyword arguments:
    archiveName -- the brain region
    neuronPages -- how many pages of the neurons we want (-1 means all pages)
    neuronsPerPage -- how many neurons per page (-1 means maximum per page)

    Note: Archive names usually start in uppercase
  """
  if (not check_api_health()): return
  if (not archiveName[0].isupper()): print "Warning: archive name does not start with upper case letter"
  numNeurons = neuronsPerPage if (neuronsPerPage != -1 and neuronsPerPage < MAX_NEURONS_PER_PAGE) else MAX_NEURONS_PER_PAGE
  url = "%s/api/neuron/select?q=archive:%s&size=%i" %(NEUROMORPHO_URL, archiveName, numNeurons)
  req = Request(url)
  response = urlopen(req)
  validate_response_code(response)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = neuronPages if (neuronPages != -1 and neuronPages < totalPages) else totalPages
  for page in xrange(0, numNeuronPages):
    url = "%s/api/neuron/select?q=archive:%s&size=%i&page=%i" %(NEUROMORPHO_URL, archiveName, numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    for neuron in xrange(0, numNeurons):
      get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])
