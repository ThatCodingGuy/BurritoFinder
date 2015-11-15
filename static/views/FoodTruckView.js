

var FoodTruckView = Backbone.View.extend({
	model: FoodTruck,
	initialize:function(options){
		this.foodTruck = options.foodTruck;
		this.map = options.map;

        this.template = _.template($('#foodTruck_template').html());
        this.render();
    },

    render: function(){
        this.$el.html(this.template({}));
        this.activate();
        return this;
    },

});

