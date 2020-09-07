#!/usr/bin/env python

from geometry_tools.geometry_tools import *
import os
import unittest

class TestGeometryTools(unittest.TestCase):
  def __compose_filename(self, filename, folder="data", extension=".swc", sep=os.path.sep):
    return "%s%s%s%s" % (folder, sep, filename, extension)

  def test_linear_cylinder_without_intersection(self):
    filename = self.__compose_filename("linearCylinders")
    self.assertFalse(check_cylinder_intersections(filename))

  def test_bended_cylinder_without_intersection(self):
    filename = self.__compose_filename("linearCylindersBended")
    self.assertFalse(check_cylinder_intersections(filename))

  def test_bended_cylinder_with_intersection(self):
    filename = self.__compose_filename("linearCylindersBendedSharpAngle")
    self.assertTrue(check_cylinder_intersections(filename))

if __name__ == '__main__':
    unittest.main()
