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

    contentString = "<div class='infowindow'>" + 
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

$(document).ready(
function()
{
    $(".toggle-source").click(
    function()
    {
        console.log("click");
        $("pre").fadeToggle(300);

        if (this.innerText[0] == "S")
        {
            this.innerText = "Hide Source Code";
        }
        else
        {
            this.innerText = "Show Source Code";
        }
    } );

    $(".toggle-table").click(
    function()
    {
        $(".sat-table-container").fadeToggle(300);
        $(".sat-head").fadeToggle(300);

        if (this.innerText[0] == "S")
        {
            this.innerText = "Hide Data";
        }
        else
        {
            this.innerText = "Show Data";
        }
    } );

    
    $(".sat-table tr").click(
    function()
    {
        var name = $(this).data("name");
        var infowindow = infowindows[name][0];
        var marker = infowindows[name][1];

        console.log(infowindow);
        console.log(marker);
        console.log(map);

        if (currently_open_infowindow)
            currently_open_infowindow.setMap(null); // close currently open infoWindow

        infowindow.open(map, marker);
        currently_open_infowindow = infowindow;
    } );

    google.maps.event.addDomListener(window, 'load', initialize);

    hljs.initHighlightingOnLoad();
} );
