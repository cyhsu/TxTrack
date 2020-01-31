var EndDate = new Date();
EndDate.setUTCMinutes(30, 0, 0);
EndDate.setHours(EndDate.getHours() - 1);

var StartDate = new Date();
StartDate.setUTCMinutes(30, 0, 0);
StartDate.setDate(StartDate.getDate() - 1);

var map = L.map('map', {
    zoom: 8,
    center: [27.855, -95.55],
    //fullscreenControl: true,
    timeDimension: true,
    timeDimensionControl: true,
    timeDimensionOptions: {
        timeInterval: StartDate.toISOString() +
                      "/" + EndDate.toISOString(),
        period: "PT1H",
        currentTime: StartDate.getTime() 
    },
    timeDimensionControlOptions: {
        autoPlay: true,
        loopButton: true,
        timeSteps: 1,
        playReverseButton: true,
        limitSliders: true,
        playerOptions: {
            buffer: 24,
            transitionTime: 250,
            loop: true,
        }
    },
});

var icon = L.icon({
    iconUrl: '/static/img/Icon_OilSpill.png',  //set the icon you want to appear
    iconSize: [22, 22],
    iconAnchor: [5, 25]
});

L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var testWMS = "http://hfrnet-tds.ucsd.edu/thredds/wms/HFR/USEGC/6km/hourly/GNOME/HFRADAR,_US_East_and_Gulf_Coast,_6km_Resolution,_Hourly_RTV_(GNOME)_best.ncd"
//var testWMS = "https://hfrnet-tds.ucsd.edu/thredds/wms/HFR/USEGC/6km/hourly/RTV/HFRADAR_US_East_and_Gulf_Coast_6km_Resolution_Hourly_RTV_best.ncd"
var testLayer = L.tileLayer.wms(testWMS, {
    layers: 'surface_sea_water_velocity',
    version: '1.3.0',
    format: 'image/png',
    transparent: true,
    styles: 'fancyvec/rainbow',
    markerscale: 15,
    markerspacing: 10,
    abovemaxcolor: "extend",
    belowmincolor: "extend",
    colorscalerange: "0,0.4",
    attribution: 'TAMU HF RADAR | sea_water_velocity'
});
/* var proxy = 'server/proxy.php';
var testTimeLayer = L.timeDimension.layer.wms(testLayer, {
    proxy: proxy,
    updateTimeDimension: true
});
testTimeLayer.addTo(map);*/

var testTimeLayer = L.timeDimension.layer.wms(testLayer, {
    updateTimeDimension: true
});
testTimeLayer.addTo(map);

var testLegend = L.control({
    position: 'topright'
});
testLegend.onAdd = function(map) {
    var src = testWMS + "?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetLegendGraphic&LAYER=surface_sea_water_velocity&PALETTE=rainbow&colorscalerange=0,0.4";
    var div = L.DomUtil.create('div', 'info legend');
    div.innerHTML +=
        '<img src="' + src + '" alt="legend">';
    return div;
};
testLegend.addTo(map);

$('#dtp_start').datetimepicker({
    inline: true,
    value: StartDate,
    // value: new Date('2019-06-01'),
    format: "c"
});
$('#dtp_end').datetimepicker({
    inline: true,
    value: EndDate,
    // value: new Date('2019-06-03'),
    format: "c"
});

$("#btn_timerange").click(function(){
    var startTime = new Date($('#dtp_start').val());
    startTime.setUTCMinutes(30, 0, 0);
    var endTime = new Date($('#dtp_end').val());
    endTime.setUTCMinutes(30, 0, 0);
    var newAvailableTimes = L.TimeDimension.Util.explodeTimeRange(startTime, endTime, 'PT1H');
    map.timeDimension.setAvailableTimes(newAvailableTimes, 'replace');
    map.timeDimension.setCurrentTime(startTime.getTime());
});

$("#btn_limitrange").click(function(){
    var startTime = new Date($('#dtp_start').val());
    startTime.setUTCMinutes(30, 0, 0);
    var endTime = new Date($('#dtp_end').val());
    endTime.setUTCMinutes(30, 0, 0);
    map.timeDimension.setLowerLimit(startTime);
    map.timeDimension.setUpperLimit(endTime);
    map.timeDimension.setCurrentTime(startTime.getTime());
});
