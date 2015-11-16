import unittest

from models.FoodTruck import FoodTruck, FoodTruckSchedule, FoodTruckManager

class FoodTruckTestCase(unittest.TestCase):

	def setUp(self):
		self.name = "Bobby's Burgers"
		self.description = "Delicious hamburgers for all"
		self.longitude=45
		self.latitude=-115
		self.weeklySchedule=[
			"11am - 7pm",
			"10am - 2pm",
			"10am - 2pm",
			"10am - 2pm",
			"10am - 2pm",
			"10am - 2pm",
			"11am - 7pm",
		]
		self.foodTruck = FoodTruck(
			name=self.name, description=self.description, 
			longitude=self.longitude, latitude=self.latitude, 
			weeklySchedule=self.weeklySchedule
			)

	def tearDown(self):
		pass

	def test_serialize(self):
		self.assertEqual({
			'name': self.name, 
			'description': self.description,
			'longitude': self.longitude,
			'latitude': self.latitude,
			'weeklySchedule': self.weeklySchedule,
		}, self.foodTruck.serialize())

