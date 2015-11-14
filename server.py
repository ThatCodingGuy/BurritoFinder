from flask import Flask, jsonify

from werkzeug.routing import FloatConverter as BaseFloatConverter

from FoodTruck import FoodTruckManager
from SFOpenDataService import SFOpenDataService

class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

app = Flask(__name__)
app.url_map.converters['float'] = FloatConverter


FoodTruckManager.registerFoodTruckFinderService(SFOpenDataService())

@app.route("/")
def index_route():
	return "Hello World!"

"""
	Returns all food trucks.
"""
@app.route("/trucks/", methods=['GET'])
def allTrucks():
	foodTrucks = FoodTruckManager.getAllFoodTrucks()

	#TODO : There has to be a way to make this cleaner.
	#I need to read up more on jsonify
	return jsonify(results=[x.serialize() for x in foodTrucks])

"""
	Returns food trucks within radius of longitude and latitude
"""
@app.route('/trucks/<float:longitude>/<float:latitude>/<float:radius>/', methods=['GET'])
def trucksInRadius(longitude, latitude, radius):

	foodTrucks = FoodTruckManager.getFoodTrucksWithinRadius(longitude, latitude, radius)

	#TODO : There has to be a way to make this cleaner.
	#I need to read up more on jsonify
	return jsonify(results=[x.serialize() for x in foodTrucks])


if __name__ == "__main__":
	app.run(debug=True)