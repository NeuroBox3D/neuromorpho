"""Making use of the REST API (NeuroMorpho.org v7) to query the database."""
# python v2 or v3
try:
  from urllib2 import urlopen, Request, URLError
except ImportError:
  from urllib.request import urlopen, Request, URLError

import re, json, sys

# pseudo-constants
NEUROMORPHO_URL = "http://neuromorpho.org"
MAX_NEURONS_PER_PAGE = 500

def validate_response_code(response):
  """Checks response code from JSON request and print warning then exits
  Keyword arguments:
  response -- response of the issued JSON request
  """
  code = response.getcode()
  # success
  if code == 200: return

  # error codes
  if code == 400:
      print("Bad request, usually wrong parameters to select queries.")
  elif code == 404:
      print("Resource not found or does not exist")
  elif code == 405:
      print("Unsupported HTTP method used (No GET or POST request).")
  elif code == 500:
      print("Internal Server Error. Contact admin for assistance.")
  sys.exit()


def check_api_health():
  """Checks if the REST API is available

  Returns true if API is available or false otherwise
  """
  url = "http://neuromorpho.org/api/health"
  req = Request(url)

  try:
    response = urlopen(req)
    if (json.loads(response.read().decode('utf-8'))['status'] != "UP"):
      print("REST API not available.")
    else:
      return True
    
  except URLError:
     print("""
          No network connectivity. A working internet connection is required.
          Check with ISP and/or your local network infrastructure for failure.
          """)
  return False

def get_num_neurons(numNeurons):
  """Get number of neurons. API can handle only up to 500 neurons per page

    Keyword arguments:
    numNeurons -- number of neurons
  """
  return numNeurons if (numNeurons != -1 and numNeurons < MAX_NEURONS_PER_PAGE) else MAX_NEURONS_PER_PAGE

def get_neuron_pages(numNeurons, totalPages):
  """
    Get the number of neuron pages. API handles up to 500 neurons per page.
    If more neurons than supported by the NeuroMorpho API (> 500), then
    multiple pages need to be retrieved, otherwise one page is retrieved.

    Keyword arguments:
    numNeurons -- number of neurons
    totalPages -- number of pages available when using numNeurons per page
  """
  return min(totalPages, numNeurons / MAX_NEURONS_PER_PAGE if numNeurons > MAX_NEURONS_PER_PAGE else 1)


def get_swc_by_filter_rule_for_search_term(filterStringList, searchTerm, numNeurons, index=-1):
  """Downloads n neurons by filterString and stores as SWC files

  Keyword arguments:
  filterString -- the filter string as key value pairs
  searchTerm -- the search term
  n -- number of neurons
  """
  if (not check_api_health()): return
  url = "%s/api/neuron/select?q=%s&" % (NEUROMORPHO_URL, searchTerm.replace("=", ":"))

  pairs = []
  if (len(filterStringList) == 1):
    filterStringList.replace(" ", "%20")
    pairs = filterStringList.split("=")
  else:
     for filterString in filterStringList:
        pairs = pairs + [fq.replace(" ", "%20").split("=") for fq in filterString]

  url = url + "&".join(["fq=%s:%s" % (k, v) for (k, v) in pairs])
  req = Request(url)
  response = urlopen(req)
  validate_response_code(response)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = get_neuron_pages(numNeurons, totalPages)
  count = 0
  for page in range(0, numNeuronPages):
    url = url + "&size=%i&page=%i" % (numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    count = 0
    for neuron in range(0, numNeurons):
      # get each file
      if index == -1: get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])

      # get only file with index in this html view
      if (neuron-count == index):
        get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])
        return neurons['_embedded']['neuronResources'][neuron]['neuron_name']
    # increase count here
    count = neuron + numNeurons

def get_swc_by_filter_rule_for_search_term_by_index(filterStringList, searchTerm, index):
  """Downloads the neuron by index which matches filter criteria and search term

  Keyword arguments:
  filterStringList -- the filter string as key value pairs
  searchTerm -- the search term
  index -- index of neuron of interest
  """
  get_swc_by_filter_rule_for_search_term(filterStringList, searchTerm, -1, index)


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
  html = urlopen(url).read().decode("utf-8")
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
     with open(fileName, 'w') as f:
        f.write(response.read().decode('utf-8'))

def get_swc_by_neuron_name(neuronName):
  """Download the SWC file specified by the neuron's name

    Keyword arguments:
    neuronName -- the neuron index in the database
  """
  if (not check_api_health()): return
  url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuronName)
  html = urlopen(url).read().decode("utf-8")
  p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
  m = re.findall(p, html)
  for match in m:
     fileName = match.replace("%20", " ").split("/")[-1]
     response = urlopen("%s/dableFiles/%s" % (NEUROMORPHO_URL, match))
     with open(fileName, 'w') as f:
        f.write(response.read().decode('utf-8'))
  return fileName


def get_swc_by_brain_region(brainRegion, numNeurons=-1):
  """Download a specific number of SWC files specified by a region name

    Keyword arguments:
    brainRegion -- the brain region
    numNeurons -- how many neurons to retrieved (-1 means all neurons)

    Note: Brain regions usually start in lowercase
  """
  if (not check_api_health()): return
  if (not brainRegion[0].islower()): print("Warning: brain region does not start with lower case letter")
  numNeurons = get_num_neurons(numNeurons)
  url = "%s/api/neuron/select?q=brain_region:%s&size=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons)
  req = Request(url)
  response = urlopen(req)
  validate_response_code(response)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = get_neuron_pages(numNeurons, totalPages)
  for page in range(0, numNeuronPages):
    url = "%s/api/neuron/select?q=brain_region:%s&size=%i&page=%i" %(NEUROMORPHO_URL, brainRegion, numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    for neuron in range(0, numNeurons):
      get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])

def get_swc_by_archive_name(archiveName, numNeurons=-1):
  """Download a specific number of SWC files specified by an archive name

    Keyword arguments:
    archiveName -- the brain region
    numNeurons -- how many neurons to retrieve (-1 means all neurons)
    Note: Archive names usually start in uppercase
  """
  if (not check_api_health()): return
  if (not archiveName[0].isupper()): print("Warning: archive name does not start with upper case letter")
  numNeurons = get_num_neurons(numNeurons)
  url = "%s/api/neuron/select?q=archive:%s&size=%i" %(NEUROMORPHO_URL, archiveName, numNeurons)
  req = Request(url)
  response = urlopen(req)
  validate_response_code(response)
  totalPages = json.loads(response.read().decode("utf-8"))['page']['totalPages']
  numNeuronPages = get_neuron_pages(numNeurons, totalPages)
  for page in range(0, numNeuronPages):
    url = "%s/api/neuron/select?q=archive:%s&size=%i&page=%i" %(NEUROMORPHO_URL, archiveName, numNeurons, page)
    req = Request(url)
    response = urlopen(req)
    neurons = json.loads(response.read().decode("utf-8"))
    numNeurons = len(neurons['_embedded']['neuronResources'])
    for neuron in range(0, numNeurons):
      get_swc_by_neuron_name(neurons['_embedded']['neuronResources'][neuron]['neuron_name'])
