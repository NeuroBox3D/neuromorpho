#!/usr/bin/env python
import unittest

class TestRestWrapper(unittest.TestCase):
  @staticmethod
  def __num_lines(filename):
    with open(filename, "r") as f:
      return sum(1 for _ in f.readlines())

  def test_get_swc_by_neuron_id(self):
    from rest_wrapper.rest_wrapper import get_swc_by_neuron_index
    get_swc_by_neuron_index(1)
    num_lines = self.__num_lines('cnic_001.CNG.swc')
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_neuron_name(self):
    from rest_wrapper.rest_wrapper import get_swc_by_neuron_name
    get_swc_by_neuron_name("cnic_001")
    num_lines = self.__num_lines('cnic_001.CNG.swc')
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_brain_region(self):
    from rest_wrapper.rest_wrapper import get_swc_by_brain_region
    get_swc_by_brain_region("neocortex", 1)
    num_lines = self.__num_lines('cnic_001.CNG.swc')
    self.assertTrue(num_lines == 1281, "SWC file incomplete!")

  def test_get_swc_by_archive_name(self):
    from rest_wrapper.rest_wrapper import get_swc_by_archive_name
    get_swc_by_archive_name("Smith", 1)
    num_lines = self.__num_lines('0-2.CNG.swc')
    self.assertTrue(num_lines == 494, "SWC file incomplete!")

  def test_get_swc_by_filter_and_search_term(self):
    from rest_wrapper.rest_wrapper import get_swc_by_filter_rule_for_search_term
    valid_filename = "H16-03-002-01-03-03_559391969_m"
    filename = get_swc_by_filter_rule_for_search_term([["cell_type=pyramidal"], \
               ["archive=Allen Cell Types"]], "brain_region:neocortex", -1, 1)
    self.assertTrue(valid_filename == filename, "Wrong file retrieved!")

  def test_api_check(self):
    from rest_wrapper.rest_wrapper import check_api_health
    status = check_api_health()
    self.assertIsNotNone(status, "API status could not be retrieved!")

if __name__ == '__main__':
    unittest.main()
