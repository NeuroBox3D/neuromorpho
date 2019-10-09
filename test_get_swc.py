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
    get_swc_by_brain_region("neocortex", 1, 1)
    num_lines = sum(1 for line in open('cnic_001.CNG.swc'))
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_archive_name(self):
    get_swc_by_archive_name("Smith", 1, 1)
    num_lines = sum(1 for line in open('0-2.CNG.swc'))
    self.assertTrue(num_lines == 494, "SWC file incomplete!")

if __name__ == '__main__':
    unittest.main()
