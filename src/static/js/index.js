var map = L.map('map', {
    zoom: 8,
    fullscreenControl: true,
    timeDimension: true,
    timeDimensionOptions: {
        timeInterval: "2019-06-01/2019-06-03",
        period: "PT1H",
        currentTime: Date.parse("2019-06-01T00:00:00Z")
    },
    timeDimensionControl: true,
    timeDimensionControlOptions: {
        autoPlay: true,
        loopButton: true,
        timeSteps: 1,
        playReverseButton: true,
        limitSliders: true,
        playerOptions: {
            buffer: 0,
            transitionTime: 250,
            loop: true,
        }
    },
    center: [27.855, -95.55],
});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var testWMS = "https://hfrnet-tds.ucsd.edu/thredds/wms/HFR/USEGC/6km/hourly/GNOME/HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd"
var testLayer = L.tileLayer.wms(testWMS, {
    layers: 'surface_sea_water_velocity',
    version: '1.3.0',
    format: 'image/png',
    transparent: true,
    styles: 'prettyvec/rainbow',
    markerscale: 15,
    markerspacing: 10,
    abovemaxcolor: "extend",
    belowmincolor: "extend",
    colorscalerange: "0,0.4",
    attribution: 'TAMU HF RADAR | sea_water_velocity'
});
var proxy = 'server/proxy.php';
var testTimeLayer = L.timeDimension.layer.wms(testLayer, {
    proxy: proxy,
    updateTimeDimension: true
});
testTimeLayer.addTo(map);

var testLegend = L.control({
    position: 'topright'
});
testLegend.onAdd = function(map) {
    var src = testWMS + "?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&LAYER=surface_sea_water_velocity&PALETTE=rainbow&colorscalerange=0,1.5";
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        '<img src="' + src + '" alt="legend">';
    return div;
};
testLegend.addTo(map);

$('#dtp_start').datetimepicker({
    inline: true,
    value: new Date('2019-06-01'),
    format: "c"
});
$('#dtp_end').datetimepicker({
    inline: true,
    value: new Date('2019-06-03'),
    format: "c"
});

// $("#btn_timerange").click(function(){
//     alert('aaaaaaa')
//     var startTime = new Date($('#dtp_start').val());
//     var endTime = new Date($('#dtp_end').val());
//     var newAvailableTimes = L.TimeDimension.Util.explodeTimeRange(startTime, endTime, 'PT1H');
//     map.timeDimension.setAvailableTimes(newAvailableTimes, 'replace');
//     map.timeDimension.setCurrentTime(startTime);
// });

$("#btn_limitrange").click(function(){
    var startTime = new Date($('#dtp_start').val());
    var endTime = new Date($('#dtp_end').val());
    map.timeDimension.setLowerLimit(startTime);
    map.timeDimension.setUpperLimit(endTime);
    map.timeDimension.setCurrentTime(startTime);
});

// document.getElementById('btn_lonlat').addEventListener("click", AddLoc()){
// $("#btn_lonlat").click(function AddLoc() {
// function AddLoc() {
$("#btn_lonlat").click(function(){
  alert('abcdefg')
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
  // submit_to_flask(site_info);
});

function submit_to_flask(site_info) {
  $.ajax({
    url: "/json",
    type: "POST",
    datatype:"json",
    contentType: "application/json",
    data: site_info,
  })
}
