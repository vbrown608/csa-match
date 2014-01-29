//Multiple markers example: http://stackoverflow.com/questions/3059044/google-maps-js-api-v3-simple-multiple-marker-example/3059129#3059129
$(document).ready(function() {
	function initialize() {
		var mapOptions = {
			center: new google.maps.LatLng(37.75, -122.28),
			zoom: 9
		};
		var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);

		var sites = [{ name: 'First Farm', lat: 37.75, lng: -122.28, info: '1', details: 'Even more information'},
		{name: 'Second Spot', lat: 37.8, lng: -122, info: '2', details: 'Like, a lot more'},
		{name: 'Third Thhh', lat: 37.75, lng: -121.95, info: '3', details: 'So much information!!!'}];
		
		var infowindow = new google.maps.InfoWindow();
		var marker;
		
		$.each(sites, function(key, data) {
			var latLng = new google.maps.LatLng(data.lat, data.lng); 
			
			// Creating a marker and putting it on the map
			marker = new google.maps.Marker({
				position: latLng,
				map: map,
				title: data.name
			});
			
			// Adding infowindows
			google.maps.event.addListener(marker, 'click', (function(marker) {
				return function() {
					infowindow.setContent(data.info);
					infowindow.open(map, marker);
				}
			})(marker));
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

	//$('input').click(function(){
		$.ajax({
			url: '/nearestSites',
			success: function(result){
	    		alert(result);
	  		}
		});
	//});
});


