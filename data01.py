#!/usr/bin/python

print "Content-type: text/html\n"
print ""

import urllib

print """
<!DOCTYPE html>
<html> <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <title>SAT Scores around NYC</title>
    <link rel="stylesheet" href="data01_style.css">
    <link href='http://fonts.googleapis.com/css?family=Lato:400,900,700italic' rel='stylesheet' type='text/css'>
    
    <script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyALc9l8tOL3WZiGQ1Av3CsLsJdZyt477KA&sensor=false"> </script>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/2.0.0/jquery.min.js"></script>
    <script src="data01_script.js"> </script>
    <script type="text/javascript">
        coordinates = new google.maps.LatLng(40.701646, -73.952);
        function initialize() {
            var mapOptions = {
                zoom: 11,
                center: coordinates,
                streetViewControl: false, 
                mapTypeControl: false,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }
            map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
"""
def valid_data(name, reading, math, writing):
    return name != "School Name" and "s" not in (reading, math, writing)

schools = []
school_locations = {}

school_locations_file = open("schools_data.csv") 
for line in school_locations_file:
    name, lat, lon = line.split(",")
    school_locations[name] = {}
    school_locations[name]["lat"] = lat
    school_locations[name]["lon"] = lon[:-1] # remove \n

sat_data_file = open("sat_data.csv")
for line in sat_data_file:
    cols = line.split(",")  
    dbn, name, takers, reading, math, writing = cols[:3] + cols[-3:]
    name = name.replace("\"", "")
    writing = writing[:-1]

    if name not in school_locations or not valid_data(name, reading, math, writing): # no geospatial data or bad data
        continue

    avg = sum(map(int, (reading, math, writing))) / 3

    schools.append({
        "name": name, \
        "dbn": dbn,\
        "takers": takers,\
        "reading": reading, \
        "math": math, \
        "writing": writing, \
        "avg": avg, \
        "lat": school_locations[name]["lat"], \
        "lon": school_locations[name]["lon"] \
    })


sorted_schools = sorted(schools, key=lambda school: school["avg"], reverse=True)
Min, Max = sorted_schools[-1]["avg"], sorted_schools[0]["avg"]
interval = Max - Min
steps = 100. / interval
    
num_schools = 0
for school in schools:
    above_min = school["avg"] - Min
    percentile = above_min * steps * 0.01

    print """
            addMarker(map, \"""" + school["name"] + """\", """ + str(school["lat"]) + """, """ + str(school["lon"]) + """, """ + str(percentile) + """, """ + str(school["reading"]) + """, """ + str(school["math"]) + """, """ + str(school["writing"]) + """);"""

    num_schools += 1
sat_data_file.close()
school_locations_file.close()

print """
        }
    </script>
</head>
<body>
    <div id="map-canvas" > </div>
    <div id="content">
        <h1>SAT Scores of NYC Public Schools </h1>
        <p>By Miad Hoque and Philipp Steinmann </p>
        <p>A visual representation of average SAT scores from """ + str(num_schools) + """ high schools around the city. </p>
    
        <button class="toggle-table">Show Data</button>
        <table class="sat-head">
            <tr>
                <th>School Name </th>
                <th>Reading </th>
                <th>Math </th>
                <th>Writing </th>
            </tr>
        </table>
        <div class="sat-table-container">
            <table class="sat-table">
                <tbody>
"""
for school in sorted_schools:
    print "                    <tr data-name=\"" + school["name"] + "\">"
    for col in (school["name"], school["reading"], school["math"], school["writing"]):
        print "                    <td>" + col + "</td>"
    print "                    </tr>"

print """
                </tbody>
            </table>
        </div>
    </div>
  </body>
</html>
"""
