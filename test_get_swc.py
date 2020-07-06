#!/usr/bin/env python
from neuromorpho import *
import unittest

class TestGetSWCMethod(unittest.TestCase):
  def test_get_swc_by_neuron_id(self):
    get_swc_by_neuron_index(1)
    num_lines = sum(1 for line in open('cnic_001.CNG.swc'))
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_neuron_name(self):
    get_swc_by_neuron_name("cnic_001")
    num_lines = sum(1 for line in open('cnic_001.CNG.swc'))
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_brain_region(self):
    get_swc_by_brain_region("neocortex", 1)
    num_lines = sum(1 for line in open('cnic_001.CNG.swc'))
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_archive_name(self):
    get_swc_by_archive_name("Smith", 1)
    num_lines = sum(1 for line in open('0-2.CNG.swc'))
    self.assertTrue(num_lines == 494, "SWC file incomplete!")

  def test_get_swc_by_filter_and_search_term(self):
    filename = get_swc_by_filter_rule_for_search_term([["cell_type=pyramidal"], ["archive=Allen Cell Types"]], "brain_region:neocortex", -1, 1)
    self.assertTrue("H16-03-002-01-03-03_559391969_m" == filename, "Wrong file retrieved!")

if __name__ == '__main__':
    unittest.main()
