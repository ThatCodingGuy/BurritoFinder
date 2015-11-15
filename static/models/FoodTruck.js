


var FoodTruck = Backbone.Model.extend({
	//Basic pojo
	initialize: function(options) {
		var foodTruck = model.attributes;
	  	this.position = {lat: foodTruck.latitude, lng: foodTruck.longitude};
	  	this.name = foodTruck.name;
	}
});

var FoodTruckCollection = Backbone.Collection.extend({
	model: FoodTruck,
	url: function () {
		return '/trucks/' + this.longitude + '/' + this.latitude + '/' + this.radius
	},
	initialize: function(models, options) {
		this.longitude = options.longitude;
		this.latitude = options.latitude;
		this.radius = options.radius;
	},

	parse: function(response) {
		return response.results
	}
})
