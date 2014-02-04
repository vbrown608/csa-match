//Multiple markers example: http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example/3059129#3059129
$(document).ready(function() {

	function initialize() {
		var mapOptions = {
			center: new google.maps.LatLng(37.85, -122.25),
			zoom: 10
		};
		var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
		
		var infowindow = new google.maps.InfoWindow();
		var marker;
		
		$.get('/nearestSites', function(result) {
			$.each(result, function(key, data) {
				console.log(data.lng)
				var latLng = new google.maps.LatLng(data.lat, data.lng); 
				
				// Creating a marker and putting it on the map
				marker = new google.maps.Marker({
					position: latLng,
					map: map,
					title: data.csa.name
				});
				
				// Adding infowindows
				google.maps.event.addListener(marker, 'click', (function(marker) {
					return function() {
						infowindow.setContent(data.desc);
						infowindow.open(map, marker);
					}
				})(marker));

				// Add site to list in sidebar
				// $('ul#site-list').prepend('<li>' + data.name + '</li>');
			});
		});
	}
	google.maps.event.addDomListener(window, 'load', initialize);

	// Convert address to latitude and longitude using Google Geocoding Service
	function searchLocations() {
		var address = document.getElementById("addressInput").value;
		var geocoder = new google.maps.Geocoder();
		geocoder.geocode({address: address}, function(results, status) {
			if (status == google.maps.GeocoderStatus.OK) {
				alert(results[0].geometry.location);
				//searchLocationsNear(results[0].geometry.location);
			} else {
				alert(address + ' not found');
			}
		});
		return false;
	}

	$('header').click( function() {
		searchLocations();
	});

});


