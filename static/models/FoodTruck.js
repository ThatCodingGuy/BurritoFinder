


var FoodTruck = Backbone.Model.extend({
	//Basic pojo
});

var FoodTruckCollection = Backbone.Collection.extend({
	model: FoodTruck,
	url: '/trucks/'
})
