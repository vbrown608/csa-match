//Multiple markers example: http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example/3059129#3059129
window.Map = {

	initialize: function(lat, lng, sites) {
		var mapOptions = {
			center: new google.maps.LatLng(lat, lng),
			zoom: 10
		};
		var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

		this.dropPins(sites, map);

		$("form").on('submit', function(e) {
			var address = $('#addressInput').val();
			var location = this.searchLocations(address);

			//stop form submission
			e.preventDefault();
		}.bind(this));
	},

	dropPins: function(data, map) {
		var infowindow = new google.maps.InfoWindow();
		var marker;

		for (var i = 0; i < data.length; i++){
			site = data[i];
			var latLng = new google.maps.LatLng(site.lat, site.lng);

			// Creating a marker and putting it on the map
			marker = new google.maps.Marker({
				position: latLng,
				map: map,
				title: site.csa.name
			});

			// Adding infowindows
			google.maps.event.addListener(marker, 'click', (function(marker) {
				return function() {
					infowindow.setContent(site.csa.desc);
					infowindow.open(map, marker);
				}
			})(marker));
		}
	},

	// Convert address to latitude and longitude using Google Geocoding Service
	searchLocations: function(address) {
		var address = document.getElementById("addressInput").value;
		var geocoder = new google.maps.Geocoder();
		var geo = geocoder.geocode({
			address: address
		}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				var lat = results[0].geometry.location.k;
				var lng = results[0].geometry.location.A;
				window.location = encodeURI('/?address=' + address + '&lat=' + lat + '&lng=' + lng);
			} else {
				// Handle failed search here.
				alert('Address not found.');
			}
		});
	}
}