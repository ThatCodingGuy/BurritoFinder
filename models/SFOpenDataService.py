import requests

from models.FoodTruck import FoodTruck

class ScheduleParseException(Exception):
    pass

class SFOpenDataService():

	def __init__(self):
		#We have the array twice in a row so we don't have to worry about module when iterating between 2 days
		self.dayTokens = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]

		self.api_endpoint = "https://data.sfgov.org/resource/rqzj-sfat.json"

	"""
		This method fetches the food trucks from the API,
		and parses them to our own format.
	"""
	def fetchFoodTrucks(self):

		#We fetch all the foodtrucks
		content = requests.get(self.api_endpoint).json()

		#We only get the ones that are currently approved
		content = filter(lambda x : x.get('status', None) == "APPROVED", content)

		foodTrucks = []
		for entry in content:
			name = entry.get('applicant', None)
			description = entry.get('fooditems', None)
			longitude = entry.get('longitude', None)
			latitude = entry.get('latitude', None)
			dayshours = entry.get('dayshours', None)

			#Check to see if the data we need is in this entry
			if name==None or description==None or longitude==None or latitude==None or dayshours==None:
				#If it's not, we skip this entry
				continue

			try:
				weeklySchedule = self.parseSchedule(dayshours)
			except ScheduleParseException:
				#We'll ignore parse exceptions, skipping unclean entries
				continue

			foodTruck = FoodTruck(name=name, description=description, longitude=float(longitude), latitude=float(latitude), weeklySchedule=weeklySchedule)
			foodTrucks.append(foodTruck)

		return foodTrucks




	"""
		This method is a helper to parse the schedules from SFData

		format : We:6AM-3PM;Su:6AM-8PM


	"""
	def parseSchedule(self, dayshours):
		
		#Each segment represents the schedule for a day or many days
		segments = dayshours.split(";")

		workingDays = {}

		for segment in segments:
			segment = segment.split(":")

			if len(segment) != 2:
				raise ScheduleParseException("A segment could not be cleanly divided in 2")

			daySegment = segment[0]
			time = segment[1]

			days = daySegment.split("/")

			for day in days:
				toAdd = self.parseDaySegment(day)

				for added in toAdd:
					workingDays[added] = time

		schedule = []
		for day in self.dayTokens:
			if day in workingDays:
				schedule.append(workingDays[day])
			else:
				schedule.append("Not open")
		return schedule



	def parseDaySegment(self, day):
		#At this point we have 2 cases.
		#Either the day is alone, or there's a dash in between.
		#We check for the dash to evaluate the 2 cases.

		days = []

		if '-' in day:

			#We know we have a range.
			dayRange = day.split('-')

			if len(dayRange) != 2:
				raise ScheduleParseException("A dayrange could not be cleanly divided in 2")

			startDay = dayRange[0]
			endDay = dayRange[1]

			if startDay not in self.dayTokens:
				raise ScheduleParseException("Start day is not a recognized day identifier")

			if endDay not in self.dayTokens:
				raise ScheduleParseException("End day is not a recognized day identifier")

			daysToAdd = []
			adding = False

			#Here we add the scheduled days together to not have to use modulo operations
			for scheduledDay in self.dayTokens+self.dayTokens:

				if scheduledDay==startDay:
					daysToAdd.append(scheduledDay)
					adding = True

				elif scheduledDay==endDay and adding==True:
					daysToAdd.append(scheduledDay)
					adding = False
					break

				elif adding==True:
					daysToAdd.append(scheduledDay)
			days = daysToAdd
		else:
			#Only add this day
			if day not in self.dayTokens:
				raise ScheduleParseException("Day is not a recognized day identifier")

			days = [day]

		return days
