$("#btn_lonlat").click(function(){
  var lon = document.getElementById('txt_longitude').value
  var lat = new $('#txt_latitude').val();
  var startTime = new Date($('#dtp_start').val())
  var endTime = new Date($('#dtp_end').val())
  var site_info = JSON.stringify({
      'lon':lon,
      'lat':lat,
      'start_time':startTime,
      'end_time':endTime,
    });
  console.log(site_info)
  submit_to_flask(site_info);
  var newAvailableTimes = L.TimeDimension.Util.explodeTimeRange(startTime, endTime, 'PT1H');
  map.timeDimension.setAvailableTimes(newAvailableTimes, 'replace');
  map.timeDimension.setCurrentTime(startTime);
});

function submit_to_flask(site_info) {
  $.ajax({
    url: "/trajectory",
    type: "POST",
    datatype:"json",
    contentType: "application/json",
    data: site_info,
    success: function(response) {
              console.log('success!!!');
              console.log(response);
            },
    error: function(error) {
              console.log(error);
            },
  })
}

var geoJsonLayer = L.geoJson(trajectory,{
    pointToLayer: function (feature, latLng) {
        if (feature.properties.hasOwnProperty('last')) {
            return new L.Marker(latLng, {
                icon: icon
            });
        }
        return L.circleMarker(latLng);
    }
});
