

"""
	This class contains some useful tools to help handle
	the geography problems we run into
"""
class GeoTools:


	"""
		This method returns a method that checks if a physicalObject is
		within radius of latitude and longitude

		longitude: float position
		latitude: float position
		radius: distance in KM
	"""
	@classmethod
	def isInRadiusClosure(cls, longitude, latitude, radius):
		assert type(longitude) is float
		assert type(latitude) is float
		assert type(radius) is float or type(radius) is int

		#A conversion factor to convert
		#KM to lattitude degrees
		latRadius = radius / 110.574

		#The maximum distance is the radius.
		max_distance = latRadius ** 2

		def isInRadius(physicalObject):
			deltaLong = longitude - physicalObject.longitude
			deltaLat = latitude - physicalObject.latitude
			distance = deltaLat**2 + deltaLong**2
			return distance < max_distance

		return isInRadius