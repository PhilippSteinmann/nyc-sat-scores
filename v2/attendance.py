#!/usr/bin/python

print "Content-type: text/html\n"
print ""

import shapefile

print """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <link rel="stylesheet" href="style.css">
    <link href='http://fonts.googleapis.com/css?family=Lato:400,900,700italic' rel='stylesheet' type='text/css'>
    <style type="text/css">
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

            interval_id = setInterval(drawNextDistrict, 200);
"""
def valid_data(name, reading, math, writing):
    return name != "School Name" and "s" not in (reading, math, writing)

schools = []
school_locations = {}

school_locations_file = open("locations_data.csv") 
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
        google.maps.event.addDomListener(window, 'load', initialize);

        districts = [];
"""

districts = {}
attendance_file = open("attendance_data.csv")
for line in attendance_file.readlines()[1:]:
    data = line.strip().split(",")
    district_str, attendance, enrollment = data

    district_num = district_str[-2:]

    if district_num.isdigit():
        district_num = str(int(district_num)) # remove leading 0's

        attendance = float(attendance[:-1])

        districts[district_num] = attendance

sorted_districts = sorted(districts.values())
Min, Max = sorted_districts[0], sorted_districts[-1]
interval = Max - Min
steps = 100. / interval

print "// " + str(Min)
print "// " + str(Max)
print "//" + str(steps)

sf = shapefile.Reader("nysd_13a/nysd.shp")
records = sf.shapeRecords()
for district in records:
    shape = district.shape
    district_num = str(district.record[0])
    attendance = districts[district_num]

    above_min = attendance - Min
    percentile = above_min * steps * 0.01
    color_factor = str(int(percentile * 255))

    print "//" + str(above_min)
    print "//" + str(percentile)
    print "//" + str(color_factor)

    javascript = """
        var coords""" + district_num + """ = ["""
            
    for index in range(len(shape.points)):
        Long, lat = shape.points[index]
        javascript += """new google.maps.LatLng(""" + str(lat) + """, """ + str(Long) + """)"""
        if index != len(shape.points) - 1:
            javascript += ""","""

    print javascript.strip().replace("\n", "").replace("\t", "") # attempt to make file smaller
    print """
        ]; 
    
    districts.push({ 
        coords: coords""" + district_num + """, 
        color_factor: """ + color_factor + """, 
        attendance: """ + str(attendance) + """,
        num: """ + district_num + """
    }); """

print """

    </script>
    <script src="script.js"> </script>
</head>
<body>
    <div id="map-canvas" > </div>
</body>
</html>
"""
