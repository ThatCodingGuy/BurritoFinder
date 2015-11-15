

var MapView = Backbone.View.extend({
	el:'#map_container',

	initialize:function(){
        this.collection = new FoodTruckCollection();
        this.template = _.template($('#map_template').html());
        this.render()   

    },

	activate: function() {
		var self = this;
		var mapOptions = {
			    center: {lat: 37.775622, lng: -122.418278},
			    zoom: 15
	  	};

	  	var mapDom = $('#map').get(0);
	  	this.map = new google.maps.Map(mapDom, mapOptions);

	  	var p = this.collection.fetch();
	  	p.done(function () {
	  		_.each(self.collection.models, function(item){

	  			item.attributes.results.forEach(function(foodTruck) {
	  				var position = {lat: foodTruck.latitude, lng: foodTruck.longitude};
	  				new google.maps.Marker({
					    position: position,
					    map: self.map,
					    title: foodTruck.name
					});
	  			});

	  		}, self);
	  	});
	},

    render: function(){
        this.$el.append(this.template({}));


        this.activate();
        return this;
    },

});

