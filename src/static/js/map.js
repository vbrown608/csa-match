//Multiple markers example: http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example/3059129#3059129
window.Map = {

	// Set up the Google Maps map
	initialize: function(lat, lng, sites) {
		var mapOptions = {
			center: new google.maps.LatLng(lat, lng),
			zoom: 10,
		};
		var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

		this.dropPins(sites, map);

		$("form").on('submit', function(e) {
			var address = $('#addressInput').val();
			var location = this.geocode(address);

			//stop form submission
			e.preventDefault();
		}.bind(this));

		this.getPins(lat, lng, map);

		return map;
	},

	getPins: function(lat, lng, map) {
		$.get('/getpins', {
				lat : lat,
				lng : lng
			},
			function(response) {
				this.dropPins(response, map)
			}.bind(this)
		);
	},

	// Add pins marking nearby CSAs to the map
	dropPins: function(data, map) {
		var infowindow = new google.maps.InfoWindow();
		var marker;

		for (var i = 0; i < data.length; i++) {
			site = data[i];
			var latLng = new google.maps.LatLng(site.lat, site.lng);

			// Creating a marker and putting it on the map
			var marker = new google.maps.Marker({
				position: latLng,
				map: map,
				title: site.csa.name
			});

			// Adding infowindows
			google.maps.event.addListener(marker, 'click', (function(marker, site) {
				return function() {
					infowindow.setContent(site.csa.desc);
					infowindow.setOptions({
						disableAutoPan: true,
						maxWidth: 100
					})
					infowindow.open(map, marker);
				}
			})(marker, site));
		}
	},

	// Convert address to latitude and longitude using Google Geocoding Service
	geocode: function(address) {
		var address = document.getElementById("addressInput").value;
		var geocoder = new google.maps.Geocoder();
		var geo = geocoder.geocode({
			address: address
		}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				console.log(results[0].geometry.location);
				var lat = results[0].geometry.location.k;
				var lng = results[0].geometry.location.D;
				this.setWindow(address, lat, lng);
				return results
			} else {
				alert('Address not found.');
			}
		}.bind(this));
	},

	// Set the window location to center on a new address
	setWindow: function(address, lat, lng) {
		window.location = encodeURI('/?address=' + address + '&lat=' + lat + '&lng=' + lng);
	}

}