from flask import Flask, jsonify, render_template
from werkzeug.routing import FloatConverter as BaseFloatConverter

from models.FoodTruck import FoodTruckManager
from models.SFOpenDataService import SFOpenDataService


#We extend the float conversion to allow negative numbers and integers
class FloatConverter(BaseFloatConverter):
    regex = r'-?\d+(\.\d+)?'

app = Flask(__name__)
app.url_map.converters['float'] = FloatConverter

#We register all the different api's we want to scrape for food trucks
FoodTruckManager.registerFoodTruckFinderService(SFOpenDataService())

#This route returns our single page app
@app.route("/")
def index_route():
	return render_template('index.html')

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


@app.after_request
def add_header(response):
    """
    	Make sure the files don't cache for development
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == "__main__":
	app.run(debug=True)