

var MapView = Backbone.View.extend({
	el:'#map_container',

	initialize:function(){
        this.template = _.template($('#map_template').html());
        this.render();   

    },

	activate: function() {
		var self = this;

		//We set san fransisco as a sensible default if geolocation
		//doesn't work
		var lat = 37.775622; 
        var lng = -122.418278;

		var mapOptions = {
			    center: {lat: parseFloat(lat), lng: parseFloat(lng)},
			    zoom: 15
	  	};

	  	var mapDom = $('#map').get(0);
	  	this.map = new google.maps.Map(mapDom, mapOptions);


	  	this.collection = new FoodTruckCollection([], {
	  		longitude: lng, 
	  		latitude: lat, 
	  		radius: 5});

	  	var p = this.collection.fetch();
	  	p.done(function () {
	  		self.collection.each(function(model) {


	  		});
	  			

	  	});
	},

    render: function(){
        this.$el.html(this.template({}));
        this.activate();
        return this;
    },

});

