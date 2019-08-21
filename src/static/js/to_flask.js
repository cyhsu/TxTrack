// document.getElementById('btn_lonlat').addEventListener("click", AddLoc()){
// $("#btn_lonlat").click(function AddLoc() {
// function AddLoc() {
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
  // alert(site_info)
  console.log(site_info)
  submit_to_flask(site_info);
});

function submit_to_flask(site_info) {
  $.ajax({
    url: "/trajectory",
    type: "POST",
    datatype:"json",
    contentType: "application/json",
    data: site_info,
    // success: L.geoJson(trajectory,{
    //     pointToLayer: function (feature, latLng) {
    //         if (feature.properties.hasOwnProperty('last')) {
    //             return new L.Marker(latLng, {
    //                 icon: icon
    //             });
    //         }
    //         return L.circleMarker(latLng);
    //     }
    // success: function(resp){
    //     console.log(resp.status);
    //   }
    success: function(response) {
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
