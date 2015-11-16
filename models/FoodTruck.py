from utils.GeoTools import GeoTools


"""
	This is our FoodTruck class.

	It's basically a POJO. (POPO in python?)

	Fields :

	description: String description of the food served
	longitude: Float
	latitude: Float
	weeklySchedule: A WeeklySchedule object representing the trucks schedule at this location
"""
class FoodTruck():
	def __init__(self, name="No name provided", description="No description provided", longitude=None, latitude=None, weeklySchedule=None):
		assert longitude != None
		assert latitude != None
		assert weeklySchedule != None

		self.name=name
		self.description=description
		self.longitude=longitude
		self.latitude=latitude
		self.weeklySchedule=weeklySchedule

	def serialize(self):
		return {
			'name': self.name, 
			'description': self.description,
			'longitude': self.longitude,
			'latitude': self.latitude,
			'weeklySchedule': self.weeklySchedule,
		}


"""
	A food truck schedule is a list of strings describing a food trucks
	schedule for every day of the week.

	Example (weekdays from 8-4 and weekends from 11-6):
	[
		"11am to 6pm",
		"8am to 4pm",
		"8am to 4pm",
		"8am to 4pm",
		"8am to 4pm",
		"8am to 4pm",
		"11am to 6pm"
	]
"""
class FoodTruckSchedule():

	sunday = 0
	monday = 1
	tuesday = 2
	wednesday = 3
	thursday = 4
	friday = 5
	saturday = 6

	def __init__(self, days=None):
		assert days != None
		assert len(days) == 7

		self.days = days



"""
	FoodTruckManager is a facade to the entire backend for getting
	foodTrucks. It takes care of fetching the food truck data
	from 3rd party APIs, as well as caching it to keep the 
	responsiveness high.
"""
class FoodTruckManager():

	foodTruckFinderServices = []

	"""
	Register a new FoodTruckFinderService

	A FoodTruckFinderService must have a fetchFoodTrucks method,
	which returns a list of FoodTruck
	"""
	@classmethod
	def registerFoodTruckFinderService(cls, service):
		assert "fetchFoodTrucks" in dir(service)
		cls.foodTruckFinderServices.append(service)

	"""
		This method return a list of all found foodTrucks.
		This is mainly used for testing.
	"""
	@classmethod
	def getAllFoodTrucks(cls):

		#TODO: Cache a list of food trucks to reduce number of requests to 3rd party APIs
		#and improve loading speed
		foodTrucks = []
		for service in cls.foodTruckFinderServices:
			#TODO: Prevent collision of food trucks between services to prevent
			#Showing the same one twice
			foodTrucks.extend(service.fetchFoodTrucks())

		return foodTrucks

	@classmethod
	def getFoodTrucksWithinRadius(cls, longitude, latitude, radius):

		#We get all food trucks
		allFoodTrucks = cls.getAllFoodTrucks()

		#We create a function that checks if the food truck is in the radius
		isInRadius = GeoTools.isInRadiusClosure(longitude, latitude, radius)

		#We want to filer only the food trucks within radius of long lat
		foodTrucks = filter(isInRadius, allFoodTrucks)
		
		return foodTrucks
			
			


