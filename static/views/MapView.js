

var MapView = Backbone.View.extend({
	el:'#map_container',

	//We define the radius to be exceedingly large.
	//Eventually, we'll want to base this on the current view size
	//to reduce the size of the requests.
	//For now though, the dataset we fetch is small enough to not matter
	radiusToFetch: 2000000,

	initialize:function(){
        this.template = _.template($('#map_template').html());
        this.render();   
    },

    update_pins: function() {
    	var self = this;

    	//We only want to recalculate for large moves
    	/*if(typeof self.lastLat !== 'undefined'){
    		var deltaLat = Math.abs(self.map.getCenter().lat() - self.lastLat) * 110.574;
    		var deltaLong = Math.abs(self.map.getCenter().lng() - self.lastLong) * 111.320 * Mathcos(self.map.getCenter().lat());

    		//If the center hasn't moved much, don't do another request.
    		if (deltaLong + deltaLat < (radiusToFetch/2 * radiusToFetch/2)) {
    			return;
    		}

    		//Otherwise, set the new center
    		self.lastLat = self.map.getCenter().lat();
    		self.lastLong = self.map.getCenter().lng();
    	}*/

    	/*if(typeof self.pins !== 'undefined'){
    		//If a collection already exists, clear all the pins
    		self.pins.map(function(foodTruckPin) {
    			foodTruckPin.marker.setMap(null);
    		});
		};*/

		this.collection = new FoodTruckCollection([], {
	  		longitude: self.map.getCenter().lng(), 
	  		latitude: self.map.getCenter().lat(), 
	  		//FIXME: This should be based on the current zoom level.
	  		radius: self.radiusToFetch});

	  	var p = this.collection.fetch();
	  	var infowindow = new google.maps.InfoWindow();
	  	p.done(function () {
	  		self.pins = []
	  		self.collection.each(function(foodTruck) {
	  			var foodTruckPin = new FoodTruckView({foodTruck: foodTruck, map: self.map, infowindow: infowindow});
	  			foodTruckPin.render();
	  			self.pins.push(foodTruckPin);
	  		});
	  			

	  	});

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

		// Create the search box and link it to the UI element.
		var input = $('#pac-input').get(0);
		var searchBox = new google.maps.places.SearchBox(input);
		this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

		// Bias the SearchBox results towards current map's viewport.
		self.map.addListener('bounds_changed', function() {
			searchBox.setBounds(self.map.getBounds());
		});

		searchBox.addListener('places_changed', function() {
			var places = searchBox.getPlaces();
		    if (places.length == 0) {
		      return;
		    }

		    //Clear out the old markers here
		    var bounds = new google.maps.LatLngBounds();
	        places.forEach(function(place) {
				if (place.geometry.viewport) {
					// Only geocodes have viewport.
					bounds.union(place.geometry.viewport);
				} else {
					bounds.extend(place.geometry.location);
				}
	      	});

		    self.map.fitBounds(bounds);
		    self.update_pins();
		});

		self.update_pins();
	},

    render: function(){
        this.$el.html(this.template({}));
        this.activate();
        return this;
    },

});

