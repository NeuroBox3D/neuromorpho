"""Making use of the REST API (NeuroMorpho.org v7, and updated to v8.5) to query the database."""

import re, sys, os, requests
    
# pseudo-constants
NEUROMORPHO_URL = "http://neuromorpho.org"
MAX_NEURONS_PER_PAGE = 500

requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass


def verify_directory(directory):
    """Verifies a directory.
    """
    
    if not os.path.isdir(directory):
        os.mkdir(directory)    
        
    

def validate_response_code(response):
    """Checks response code from JSON request and print warning then exits
  Keyword arguments:
  response -- response of the issued JSON request
  """
    code = response.status_code
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
    
    reply = requests.get(url, verify=False)
    if reply.json()['status'] != "UP":
        print("REST API not available.")
        return False
    else:
        return True

def get_num_neurons(num_neurons):
    """Get number of neurons. API can handle only up to 500 neurons per page

    Keyword arguments:
    num_neurons -- number of neurons
  """
    return num_neurons if (num_neurons != -1 and num_neurons < MAX_NEURONS_PER_PAGE) else MAX_NEURONS_PER_PAGE


def get_neuron_pages(num_neurons, total_pages):
    """
    Get the number of neuron pages. API handles up to 500 neurons per page.
    If more neurons than supported by the NeuroMorpho API (> 500), then
    multiple pages need to be retrieved, otherwise one page is retrieved.

    Keyword arguments:
    num_neurons -- number of neurons
    total_pages -- number of pages available when using numNeurons per page
  """
    return min(total_pages, num_neurons / MAX_NEURONS_PER_PAGE if num_neurons > MAX_NEURONS_PER_PAGE else 1)


def get_swc_by_filter_rule_for_search_term(filter_string_list, search_term, num_neurons, index=-1, output_dir=""):
    """Downloads n neurons by filterString and stores as SWC files

  Keyword arguments:
  filter_string_list -- the filter string as key value pairs
  search_term-- the search term
  num_neurons -- number of neurons
  output_dir: the output directory where the swc files will be written
  """
    if not check_api_health(): return
    url = "%s/api/neuron/select?q=%s&" % (NEUROMORPHO_URL, search_term.replace("=", ":"))

    pairs = []
    if len(filter_string_list) == 1:
        filter_string_list.replace(" ", "%20")
        pairs = filter_string_list.split("=")
    else:
        for filterString in filter_string_list:
            pairs = pairs + [fq.replace(" ", "%20").split("=") for fq in filterString]

    url = url + "&".join(["fq=%s:%s" % (k, v) for (k, v) in pairs])
    reply = requests.get(url, verify=False)
    validate_response_code(reply)
    total_pages = reply.json()['page']['totalPages']
    num_neuron_pages = get_neuron_pages(num_neurons, total_pages)
    count = 0
    for page in range(0, num_neuron_pages):
        url = url + "&size=%i&page=%i" % (num_neurons, page)
        reply = requests.get(url, verify=False)
        neurons = reply.json()
        num_neurons = len(neurons['_embedded']['neuronResources'])
        count = 0
        for neuron in range(0, num_neurons):
            # get each file
            if index == -1: 
                get_swc_by_neuron_name(search_term, neurons['_embedded']['neuronResources'][neuron]['neuron_name'], output_dir=output_dir)

            # get only file with index in this html view
            if neuron - count == index:
                get_swc_by_neuron_name(search_term, neurons['_embedded']['neuronResources'][neuron]['neuron_name'], output_dir=output_dir)
                return neurons['_embedded']['neuronResources'][neuron]['neuron_name']
        # increase count here
        count = neuron + num_neurons


def get_swc_by_filter_rule_for_search_term_by_index(filterStringList, searchTerm, index):
    """Downloads the neuron by index which matches filter criteria and search term

  Keyword arguments:
  filterStringList -- the filter string as key value pairs
  searchTerm -- the search term
  index -- index of neuron of interest
  """
    get_swc_by_filter_rule_for_search_term(filterStringList, searchTerm, -1, index)


def get_swc_by_neuron_index(neuronIndex, output_dir):
    """Download a neuron by index and store it into a SWC file

    Keyword arguments:
    neronIndex -- the neuron index in the database
  """
    if not check_api_health(): return
    url = "%s/api/neuron/id/%i" % (NEUROMORPHO_URL, neuronIndex)
    reply = requests.get(url, verify=False)
    
    validate_response_code(reply)
    
    neuron_name = reply.json()['neuron_name']
    url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuron_name)
    reply = requests.get(url, verify=False)
    html = reply.content.decode("utf-8")
    p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
    m = re.findall(p, html)
    for match in m:
        file_name = "%s/%s" % (output_dir, match.replace("%20", " ").split("/")[-1])
        reply = requests.get(url="%s/dableFiles/%s" % (NEUROMORPHO_URL, match), verify=False)
        with open(file_name, 'w') as f:
            f.write(reply.content.decode('utf-8'))


def get_swc_by_neuron_name(directory, neuron_name, output_dir):
    """Download the SWC file specified by the neuron's name

    Keyword arguments:
    neuron_name-- the neuron index in the database
  """
    if not check_api_health(): return
    url = "%s/neuron_info.jsp?neuron_name=%s" % (NEUROMORPHO_URL, neuron_name)
    reply = requests.get(url, verify=False)
    html = reply.content.decode('utf-8')
    p = re.compile(r'<a href=dableFiles/(.*)>Morphology File \(Standardized\)</a>', re.MULTILINE)
    m = re.findall(p, html)
    file_name = None
    for match in m:
        file_name = match.replace("%20", " ").split("/")[-1]
        reply = requests.get(url="%s/dableFiles/%s" % (NEUROMORPHO_URL, match), verify=False)
        verify_directory(directory="%s/%s" % (output_dir, directory))
        
        with open('%s/%s/%s' % (output_dir, directory, file_name), 'w') as f:
            f.write(reply.content.decode("utf-8"))
            
    # check for file name presence in database
    if not file_name:
        print("Neuron with name %s not found in NeuroMorpho.org database." % neuron_name)
        return

    return file_name


def get_swc_by_brain_region(brain_region, num_neurons=-1, output_dir=""):
    """Download a specific number of SWC files specified by a region name

    Keyword arguments:
    brain_region -- the brain region
    num_neurons -- how many neurons to retrieved (-1 means all neurons)
    output_dir: the output directory where the swc files will be written

    Note: Brain regions usually start in lowercase
  """
    # check for API health
    if not check_api_health():
        return

    # check if brain region found
    if not brain_region[0].islower():
        print("Warning: brain region does not start with lower case letter")
        return

    num_neurons = get_num_neurons(num_neurons)
    url = "%s/api/neuron/select?q=brain_region:%s&size=%i" % (NEUROMORPHO_URL, brain_region, num_neurons)
    reply = requests.get(url, verify=False)
    validate_response_code(reply)
    total_pages = reply.json()['page']['totalPages']
    num_neuron_pages = get_neuron_pages(num_neurons, total_pages)
    for page in range(0, num_neuron_pages):
        url = "%s/api/neuron/select?q=brain_region:%s&size=%i&page=%i" % (
            NEUROMORPHO_URL, brain_region, num_neurons, page)
        reply = requests.get(url, verify=False)
        neurons = reply.json()
        num_neurons = len(neurons['_embedded']['neuronResources'])
        for neuron in range(0, num_neurons):
            get_swc_by_neuron_name(brain_region, neurons['_embedded']['neuronResources'][neuron]['neuron_name'], output_dir=output_dir)


def get_swc_by_archive_name(archive_name, num_neurons=-1, output_dir=""):
    """Download a specific number of SWC files specified by an archive name

    Keyword arguments:
    archive_name -- the brain region
    num_neurons -- how many neurons to retrieve (-1 means all neurons)
    output_dir: the output directory where the swc files will be written

    Note: Archive names usually start in uppercase
  """
    # check for API health
    if not check_api_health():
        return
    # check for archive name in database
    if not archive_name[0].isupper():
        print("Warning: archive name does not start with upper case letter")
        return
    
    num_neurons = get_num_neurons(num_neurons)
    url = "%s/api/neuron/select?q=archive:%s&size=%i" % (NEUROMORPHO_URL, archive_name, num_neurons)
    reply = requests.get(url, verify=False)
    validate_response_code(reply)
    total_pages = reply.json()['page']['totalPages']
    num_neuron_pages = get_neuron_pages(num_neurons, total_pages)
    for page in range(0, num_neuron_pages):
        url = "%s/api/neuron/select?q=archive:%s&size=%i&page=%i" % (NEUROMORPHO_URL, archive_name, num_neurons, page)
        reply = requests.get(url, verify=False)
        neurons = reply.json()
        num_neurons = len(neurons['_embedded']['neuronResources'])
        for neuron in range(0, num_neurons):
            get_swc_by_neuron_name(archive_name, neurons['_embedded']['neuronResources'][neuron]['neuron_name'], output_dir=output_dir)