#!/usr/bin/python

print "Content-type: text/html\n"
print ""

print """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
        html { height: 100% }
        body { height: 100%; margin: 0; padding: 0 }
        #map-canvas { height: 100% }
    </style>
    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyALc9l8tOL3WZiGQ1Av3CsLsJdZyt477KA&sensor=false">
    </script>
    <script type="text/javascript">
    coordinates = new google.maps.LatLng(40.701646, -73.952);
    function initialize()
    {
        var mapOptions = {
            zoom: 11,
            center: coordinates,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        
        var ctaLayer = new google.maps.KmlLayer({
            url: 'http://lisa.stuy.edu/~philipp.steinmann/sat/v1.5/districts.kml'
        });
        ctaLayer.setMap(map);
    }
    google.maps.event.addDomListener(window, 'load', initialize);
    </script>
</head>
<body>
    <div id="map-canvas" > </div>
</body>
</html>
"""
