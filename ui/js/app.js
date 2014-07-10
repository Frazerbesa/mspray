var App = {
    SPRAY_DAYS_URI: "http://api.mspray.onalabs.org/spraydays.json",
    BUFFER_URI: "http://api.mspray.onalabs.org/households.json?buffer=true",
    TARGET_AREA_URI: "http://api.mspray.onalabs.org/targetareas.json",
    HOUSEHOLD_URI: "http://api.mspray.onalabs.org/households.json",
    hhOptions: {
        radius: 4,
        fillColor: "#FFDC00",
        color: "#222",
        weight: 1,
        opacity: 1,
        fillOpacity: 1
    },
    sprayOptions: {
        radius: 4,
        fillColor: "#2ECC40",
        color: "#222",
        weight: 1,
        opacity: 1,
        fillOpacity: 1
    },
    sprayAltOptions: {
        weight: 2,
        opacity: 0.1,
        color: 'black',
        fillOpacity: 0.4
    },
    locationParams: function () {
        var i, params = location.search.substring(1).split("&");
        obj = {};

        for(i = 0; i < params.length; i++){
            var param = params[i].split("=");

            if(param.length > 1){
                var key = param[0], val = param[1];

                if(val.length > 1 && val[val.length - 1] == "/"){
                    val = val.slice(0, val.length - 1);
                }
                obj[key] = val;
            }
        }

        return obj;
    },
    getDay: function () {
        return this.locationParams().day;
    },
    loadHouseholds: function(map) {
        var households = L.mapbox.featureLayer()
            .loadURL(App.HOUSEHOLD_URI);

        households.on('ready', function(){
            var geojson = households.getGeoJSON();

            L.geoJson(geojson, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, App.hhOptions);
                }
            })
            .addTo(map);
        });
    },
    
    loadBufferAreas: function(map) {
        var hh_buffers = L.mapbox.featureLayer()
            .loadURL(App.BUFFER_URI);

        hh_buffers.on('ready', function(){
            var geojson = hh_buffers.getGeoJSON();

            var areaLayer = L.geoJson(geojson, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, App.hhOptions);
                },
                style: App.hhOptions,
                onEachFeature: function(feature, layer){
                    layer.on({
                        mouseover: function(e){
                            var layer = e.target;
                            k = layer;
                            // App.getHouseholdsFor(layer);
                            layer.setStyle({
                                weight: 3,
                                color: '#fff',
                                dashArray: '',
                                fillOpacity: 0.7
                            });
                        },
                        mouseout: function(e){
                        	//mouseOut = { fillOpacity: 0, weight:0 };
                            //areaLayer.setStyle(mouseOut);
                            areaLayer.resetStyle(e.target);
                            console.log("Hovered out!");
                        }
                    });
                }
            })
            .addTo(map);
        });
    },
    loadSprayPoints: function (map, day) {
        var url = App.SPRAY_DAYS_URI;
        if(day !== undefined){
            url = url += "?day=" + day;
        }
        var sprayed = L.mapbox.featureLayer()
            .loadURL(url);

        sprayed.on('ready', function(){
            var geojson = sprayed.getGeoJSON();

            L.geoJson(geojson, {
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, App.sprayOptions);
                }
			})
            .addTo(map);
        });
    },
    
    loadGoogleMapLayer: function(){
    	var map = new google.maps.Map(document.getElementById('map'), {
		    center: new google.maps.LatLng(40.718217,-73.998284),
		    zoom: 13,
		    mapTypeId: google.maps.MapTypeId.ROADMAP
		});    	
    },
    
    clearMapLayers: function(layer){
    	
    },

    getHouseholdsFor: function (layer) {
        var uri = this.HOUSEHOLD_URI;
        post_data = {in_bbox: layer.getBounds().toBBoxString()};
        $.getJSON(uri, post_data, function(data){
            console.log(data);
        });
    },

    init: function (){
        var map = L.mapbox.map('map', 'examples.map-i86nkdio')
            .setView([-15.2164, 28.2315], 15);

        var target_area = L.mapbox.featureLayer()
            .loadURL(App.TARGET_AREA_URI)
            .addTo(map);
        
        //this.loadSprayPoints(map, this.getDay()); // Loads default day in URL
        this.loadHouseholds(map);
        this.loadBufferAreas(map);
        
        $(document).ready(function(){
            var spray_lnk = $("#legend ul li a");
            
            spray_lnk.click(function(e){
                var spray_day = $(this).attr("href").slice(-1);
                
                App.loadSprayPoints(map, spray_day);
            });
        });
    }
};

App.init();
