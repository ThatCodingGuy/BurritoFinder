import unittest

from utils.GeoTools import GeoTools

"""
	This is a POJO used for testing GeoTools methods
"""
class PhysicalObject():
	def __init__(self, longitude, latitude):
		self.longitude = longitude
		self.latitude = latitude

class GeoToolsTestCase(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_isInRadiusClosure_in_radius(self):
		#We define the isInRadius function
		longitude = -75.665030
		latitude = 45.434849
		radius = 2.0
		isInRadius = GeoTools.isInRadiusClosure(longitude, latitude, radius)

		#We pick a point about 1km away
		longitude = -75.659743
		latitude = 45.428984


		#We check if the point is in the radius
		result = isInRadius(PhysicalObject(longitude, latitude))
		self.assertEqual(True, result)

	def test_isInRadiusClosure_out_radius(self):
		#We define the isInRadius function
		longitude = -75.665030
		latitude = 45.434849
		radius = 0.5
		isInRadius = GeoTools.isInRadiusClosure(longitude, latitude, radius)

		#We pick a point about 1km away
		longitude = -75.659743
		latitude = 45.428984


		#We check if the point is in the radius
		result = isInRadius(PhysicalObject(longitude, latitude))
		self.assertEqual(False, result)
		
if __name__ == '__main__':
	unittest.main()