

var FoodTruckView = Backbone.View.extend({
	model: FoodTruck,

	initialize:function(options){
		this.foodTruck = options.foodTruck;
		this.map = options.map;
		this.infowindow = options.infowindow;

		//The template here is what appears in the popup box
        this.template = _.template($('#foodTruck_template').html());
   },

    render: function(){

    	var self = this;
      	self.marker = new google.maps.Marker({
		    position: {lat: self.foodTruck.get('latitude'), lng: self.foodTruck.get('longitude')},
		    map: self.map,
		    title: self.foodTruck.get("name")
		});

      	//When the marker is clicked, open the popup with more information
	    google.maps.event.addListener(self.marker, 'click', function() {
		    self.infowindow.setContent(self.template({
		    	name: self.foodTruck.get("name"), 
		    	description: self.foodTruck.get("description"),
		    	sunday: self.foodTruck.get("weeklySchedule")[0],
		    	monday: self.foodTruck.get("weeklySchedule")[1],
		    	tuesday: self.foodTruck.get("weeklySchedule")[2],
		    	wednesday: self.foodTruck.get("weeklySchedule")[3],
		    	thursday: self.foodTruck.get("weeklySchedule")[4],
		    	friday: self.foodTruck.get("weeklySchedule")[5],
		    	saturday: self.foodTruck.get("weeklySchedule")[6],
		    }));
		    self.infowindow.open(self.map, self.marker);
	  	});
    },

});

