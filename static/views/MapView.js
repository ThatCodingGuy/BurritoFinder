

var MapView = Backbone.View.extend({
	//We define the radius to be exceedingly large.
	//Eventually, we'll want to base this on the current view size
	//to reduce the size of the requests.
	//For now though, the dataset we fetch is small enough to not matter
	radiusToFetch: 2000000,
	standardZoomLevel: 16,

	//MapView constructor(ish)
	initialize:function(options){
        this.template = _.template($('#map_template').html());
        this.initLat = options.lat;
        this.initLng = options.lng;
        //We maintain a list of loaded pins
		this.pins = [];

        //We want to render the map upon initialization
        this.render();   
    },

    //Renders the map and the pins inside
    render: function(){
    	//Replace the dom in our view by a fresh template
        this.$el.html(this.template({}));

        //Load and display all the data
        this.activate();
        return this;
    },

    //Moves the center of the map to lattitude/longitude
    move_center: function(latitude, longitude) {
    	this.map.setCenter(new google.maps.LatLng( latitude, longitude ) );
    },

    //Fetch all the food trucks and update the pins with them.
    //This method should be improved to only fetch the pins near
    //the current map view, as the current approach will quickly hit
    //scalability issues
    update_pins: function() {
    	var self = this;

    	//Clear the previous pins
    	self.pins.map(function(pin) {
    		pin.map.setMap(null);
    	});
    	self.pins = []

    	//Create a collection of food trucks with a radius from
    	//a certain position
		this.collection = new FoodTruckCollection([], {
	  		longitude: self.map.getCenter().lng(), 
	  		latitude: self.map.getCenter().lat(), 
	  		radius: self.radiusToFetch});

		//We only keep 1 infowindow so that when we open a new
		//one by clicking on a pin, it simply moves instead
		//of opening a new one
		var infowindow = new google.maps.InfoWindow();

		//Get the food truck info
	  	var p = this.collection.fetch();	
	  	p.done(function () {	  		
	  		self.collection.each(function(foodTruck) {

	  			//We create a new view for every pin
	  			var foodTruckPin = new FoodTruckView({foodTruck: foodTruck, map: self.map, infowindow: infowindow});
	  			foodTruckPin.render();

	  			self.pins.push(foodTruckPin);
	  		});
	  			

	  	});

    },

    //Initilizes the DOM in the loaded template
    //and invokes the pin loading
	activate: function() {
		var self = this;

		//Load the map based on initial positioning
		var lat = self.initLat;
        var lng = self.initLng;

        //The zoom here is arbitrary, might want to be factored into a  const
		var mapOptions = {
			    center: {lat: parseFloat(lat), lng: parseFloat(lng)},
			    zoom: self.standardZoomLevel
	  	};

	  	//Fetch the DOM elements
	  	var mapDom = $('#map').get(0);
	  	var input = $('#pac-input').get(0);

	  	//Initialize the map
	  	this.map = new google.maps.Map(mapDom, mapOptions);

		// Create the search box and link it to the UI element.
		var searchBox = new google.maps.places.SearchBox(input);
		this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

		// Bias the SearchBox results towards current map's viewport.
		self.map.addListener('bounds_changed', function() {
			searchBox.setBounds(self.map.getBounds());
		});

		//Whenever a search is issued, move the map to the new position and reload the
		//pins.
		searchBox.addListener('places_changed', function() {
			var places = searchBox.getPlaces();
		    if (places.length == 0) {
		      return;
		    }

		    var bounds = new google.maps.LatLngBounds();
	        places.forEach(function(place) {
				if (place.geometry.viewport) {
					// Only geocodes have viewport.
					bounds.union(place.geometry.viewport);
				} else {
					bounds.extend(place.geometry.location);
				}
	      	});

	        //Resize the map
		    self.map.fitBounds(bounds);
		    self.map.setZoom(self.standardZoomLevel);

		    
		    self.update_pins();
		});

		self.update_pins();
	},



});

