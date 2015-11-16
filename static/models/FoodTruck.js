


var FoodTruck = Backbone.Model.extend({
	//Basic pojo
	//The fields are
	// lattitude : float
	// longitude : float
	// name : string
	// description : string
	// weekly schedule : array of string schedule of length 7, representing opening hours from Sunday - Saturday
	initialize: function(options) {
	  	this.position = {lat: this.get("latitude"), lng: this.get("longitude")};
	}
});

var FoodTruckCollection = Backbone.Collection.extend({
	model: FoodTruck,

	//The URL to fetch the food trucks from
	url: function () {
		return 'trucks/' + this.longitude + '/' + this.latitude + '/' + this.radius
	},

	initialize: function(models, options) {
		this.longitude = options.longitude;
		this.latitude = options.latitude;
		this.radius = options.radius;
	},

	//Since the server returns everything in the results entry,
	//this make the responses easier to manipulate
	parse: function(response) {
		return response.results
	}
})
