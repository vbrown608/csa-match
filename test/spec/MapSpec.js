describe("Map", function() {
	var pins;
	var map;

  beforeEach(function() {
  	pins = [{"address": "1580 Solano Ave., Albany, CA 94707", "csa": {"desc": "Frog Hollow Farm's Happy Child CSA.", "name": "Frog Hollow Farm"}, "lng": -122.2846776, "lat": 37.8909579}];
  
  	spyOn(window.Map, "dropPins")
  	map = window.Map.initialize(37.8909579, -122.28467760000001, pins);
  });

	it("adds pins", function() {
		expect(window.Map.dropPins).toHaveBeenCalledWith(pins, map);
	});

});

describe("Results", function() {
	var results;

  beforeEach(function() {
  	results = $("ul#site-list li");
  });

	it("contain eight sites", function() {
		expect(results.length).toBe(8);
	});

	it("start with Frog Hollow Farm", function() {
		var firstLabel = $(results[0]).find('h3').text()
		expect(firstLabel).toBe("Frog Hollow Farm ");
	});
});