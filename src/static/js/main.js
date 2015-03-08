window.CSA = {
	initialize: function(sites) {
		this.handlers.initialize();
	},

	handlers: {
		initialize: function(){
			this.csaNameHandlers();
		},

		csaNameHandlers: function() {
			$('#site-list .csa').click(function(el) {
				console.log(this);
			})
		}
	}
}