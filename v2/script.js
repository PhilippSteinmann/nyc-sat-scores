function drawNextDistrict()
{
    next_district = districts.pop();
    if (districts.length == 0)
    {
        clearInterval(interval_id);
    }

    var coords = next_district["coords"];
    var color_factor = next_district["color_factor"];
    var attendance = next_district["attendance"];
    var district_num = next_district["num"];

    var district_poly = new google.maps.Polygon({
        paths: coords,
        strokeColor: "rgb(0,0,0)",
        strokeOpacity: 0.2,
        strokeWeight: 2,
        fillColor: "rgb(" + (255 - color_factor).toString() + ", " + color_factor + ", 0)",
        fillOpacity: 1
    } );

    district_poly.setMap(map);

    var contentString = "<div class='infowindow'>" +
                    "   <h3>District " + district_num + "</h3>" +
                    "   <p>" + attendance + "% Attendance</p>" +
                    "</div>";


    var infowindow = new google.maps.InfoWindow( {
        content: contentString
    } );

    google.maps.event.addListener(district_poly, "click", 
    function(event)
    {
        if (currently_open_infowindow)
            currently_open_infowindow.setMap(null);
        currently_open_infowindow = infowindow;
        infowindow.setPosition(event.latLng);
        infowindow.open(map);
    } );
}

currently_open_infowindow= null

var infowindows = {};

function addMarker(map, school_name, lat, long, percentile, reading, math, writing)
{
    var blue = 0;
    if (percentile >= 0.7)
    {
        var red = 79;
        var green = 196;
        blue = 0;
    }

    else if (percentile >= 0.3)
    {
        var red = 160;
        var green = 196;
        blue = 0;
    }

    else if (percentile >= 0.085)
    {
        var red = 205;
        var green = 165;
    }

    else if (percentile >= 0.05)
    {
        var red = 205;
        var green = 0;
    }

    else
    {
        var green = 0;
        var red = 40;
    }

    var marker = new google.maps.Marker( { 
        position: new google.maps.LatLng(lat, long),
        map: map,
        icon: {
            path: google.maps.SymbolPath.CIRCLE,
            strokeColor: "rgb(" + red + ", " +  green + ", " + blue + ")",
            strokeOpacity: 1,
            scale: 7 
        },
        title: school_name
    } );

    var contentString = "<div class='infowindow'>" + 
                    "   <h3>" + school_name + "</h3>" +
                    "   <p>" + (100 *(Math.round(percentile * 1000) / 1000)).toString().substring(0, 4) + "th Percentile" +
                    "   <table>" +
                    "       <tr>" +
                    "           <td>Reading</td>" + 
                    "           <td>" + reading + "</td>" +
                    "       </tr>" +
                    "       <tr>" +
                    "           <td>Math</td>" + 
                    "           <td>" + math + "</td>" +
                    "       </tr>" +
                    "       <tr>" +
                    "           <td>Writing</td>" + 
                    "           <td>" + writing + "</td>" +
                    "       </tr>" +
                    "   </table>" +
                    "</div>"

    var infowindow = new google.maps.InfoWindow( {
        content: contentString
    } );

    infowindows[school_name] = [infowindow, marker]

    google.maps.event.addListener(marker, "click", 
    function()
    {
        if (currently_open_infowindow)
            currently_open_infowindow.setMap(null);
        currently_open_infowindow = infowindow;
        infowindow.open(map, marker);
    } );
}
