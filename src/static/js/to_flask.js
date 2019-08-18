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
    success: function(resp){
        console.log(resp.data);
      }
  })
}
