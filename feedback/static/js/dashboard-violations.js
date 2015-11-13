$(document).ready(function () {

  "use strict";

  //all the vars, to satisfy the linter.

  var apiStatus = parseInt($('#api-health').text(), 10),
      apiModal = $('[data-remodal-id=modal]').remodal(),
      green = "rgba(76, 216, 132, 1)",
      t_green = "rgba(76, 216, 132, 0.2)",
      yellow = "rgba(245, 201, 61, 1)",
      t_yellow = "rgba(245, 201, 61, 0.2)",
      orange = "rgba(243, 155, 121, 1)",
      t_orange = "rgba(243, 155, 121, 0.2)",
      purple = "rgba(61, 51, 119, 1)",
      t_purple = "rgba(61, 51, 119, 0.2)",
      purple_1 = 'rgba(172, 75, 173, 1)',
      t_purple_1 = 'rgba(172, 75, 173, 0.2)',
      purple_2 = 'rgba(122, 0, 134, 1)',
      t_purple_2 = 'rgba(122, 0, 134, 0.2))',
      purple_3 = 'rgba(75, 0, 94, 1)',
      t_purple_3 = 'rgba(75, 0, 94, 0.2)',
      purple_4 = 'rgba(219, 172, 217, 1)',
      t_purple_4 = 'rgba(219, 172, 217, 0.2)',
      blue = 'rgba(93, 205, 252,1)';

  /************************* API health check *************************/

  window.REMODAL_GLOBALS = {
    NAMESPACE: 'modal',
    DEFAULTS: {
      hashTracking: false
    }
  };

  if(apiModal !== undefined) {

    if(apiStatus === -1) {

    //county error.
    $('.remodal').find('#status').text("Uhoh, something went wrong!");
    $('.remodal').find('p').text("It looks like we've had a problem with our data. Check back later for an update.");
    apiModal.open();

    } else if(apiStatus === 1) {

      //mostly so I can test the modals
      $('.remodal').find('#status').text("All is well.");

    } else {

      //http error code.
      $('.remodal').find('#status').text("Uhoh, something went wrong!");
      $('.remodal').find('p').text("It looks like our Socrata link is down (error" + apiStatus + "). Check back later for an update.");
      apiModal.open();

    }

  }

  /************************* dashboard css *************************/

  $('.headline').each(function() {

    var h = $(this).height(),
        container = $(this).parent().find('.content-container'),
        details = $(this).parent().find('.details'),
        offset;

    //console.log('headline is ', h, details.height() )
    //a single line of text is 25px high.
    //if we have a 2x tall headline, need to reposition .details
    //we do this by adjusting .content-container height
    if(h > 25) {

      offset = 300 - h - details.height() * 2 - 26;  //300 is fixed height, 20 is padding
      $(container).css('height', offset);

    }

    $(details).removeClass("invisible-button");

  });

  /***************************** CHARTS! *****************************/

  //charts.js defaults
  Chart.defaults.global = {
    // Boolean - Whether to animate the chart
    animation: false,

    // Boolean - If we should show the scale at all
    showScale: true,

    // Boolean - If we want to override with a hard coded scale
    scaleOverride: false,

    // String - Colour of the scale line
    scaleLineColor: "rgba(0,0,0,.1)",

    // Number - Pixel width of the scale line
    scaleLineWidth: 1,

    // Boolean - Whether to show labels on the scale
    scaleShowLabels: true,

    // Interpolated JS string - can access value
    scaleLabel: "<%=value%>",

    // Boolean - Whether the scale should stick to integers, not floats even if drawing space is there
    scaleIntegersOnly: true,

    // Boolean - Whether the scale should start at zero, or an order of magnitude down from the lowest value
    scaleBeginAtZero: true,

    // String - Scale label font declaration for the scale label
    scaleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",

    // Number - Scale label font size in pixels
    scaleFontSize: 12,

    // String - Scale label font weight style
    scaleFontStyle: "normal",

    // String - Scale label font colour
    scaleFontColor: "#666",

    // Boolean - whether or not the chart should be responsive and resize when the browser does.
    responsive: false,

    // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
    maintainAspectRatio: true,

    // Boolean - Determines whether to draw tooltips on the canvas or not
    showTooltips: true,

    // Function - Determines whether to execute the customTooltips function instead of drawing the built in tooltips (See [Advanced - External Tooltips](#advanced-usage-custom-tooltips))
    customTooltips: false,

    // Array - Array of string names to attach tooltip events
    tooltipEvents: ["mousemove", "touchstart", "touchmove"],

    // String - Tooltip background colour
    tooltipFillColor: "rgba(0,0,0,0.8)",

    // String - Tooltip label font declaration for the scale label
    tooltipFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",

    // Number - Tooltip label font size in pixels
    tooltipFontSize: 14,

    // String - Tooltip font weight style
    tooltipFontStyle: "normal",

    // String - Tooltip label font colour
    tooltipFontColor: "#fff",

    // String - Tooltip title font declaration for the scale label
    tooltipTitleFontFamily: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif",

    // Number - Tooltip title font size in pixels
    tooltipTitleFontSize: 14,

    // String - Tooltip title font weight style
    tooltipTitleFontStyle: "bold",

    // String - Tooltip title font colour
    tooltipTitleFontColor: "#fff",

    // Number - pixel width of padding around tooltip text
    tooltipYPadding: 6,

    // Number - pixel width of padding around tooltip text
    tooltipXPadding: 6,

    // Number - Size of the caret on the tooltip
    tooltipCaretSize: 8,

    // Number - Pixel radius of the tooltip border
    tooltipCornerRadius: 6,

    // Number - Pixel offset from point x to tooltip edge
    tooltipXOffset: 10,

    // String - Template string for single tooltips
    tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= value %>",

    // String - Template string for multiple tooltips
    multiTooltipTemplate: "<%= value %>",

    // Function - Will fire on animation progression.
    onAnimationProgress: function(){ /* empty */ },

    // Function - Will fire on animation completion.
    onAnimationComplete: function(){ /* empty */  }
  };

  /* Permitting & violations */

  var 
      ctx3 = $("#violations").get(0).getContext("2d"),
      permitJSON = JSON.parse($("#permits_rawjson")[0].childNodes[0].data),
      violationsJSON = JSON.parse($("#violations_rawjson")[0].childNodes[0].data),
      series2 = [],
      datetime2 = [],
      series3 = [],
      datetime3 = [],
      openPermitData,
      openPermitDataset,
      openPermitChart;

  buildViolationsCharts();



  function buildViolationsCharts() {

    for(var i = 0; i < violationsJSON.length; i++) {

      //console.log(violationsJSON[i]);

      series3.push(violationsJSON[i].total);
      datetime3.push(prettyDates((violationsJSON[i].month).split('T')[0]));

    }

    series3.reverse();
    datetime3.reverse();

    var d3 = {
        labels:datetime3,
        datasets: [
          {
            fillColor: t_orange,
            strokeColor: orange,
            pointColor: orange,
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: purple,
            data: series3
          }
        ]
      },

      newLineChart = new Chart(ctx3).Line(d3);

  }

  function prettyDates(date) {

    var year = date.split('-')[0];
    var month = String(date.split('-')[1]);   //strict mode means no octal literals -- no 08 or 09 unless type string. A thing I learned today!

    switch (month) {

      case '01':
        month = 'Jan';
        break;
      case '02':
        month = 'Feb';
        break;
      case '03':
        month = 'Mar';
        break;
      case '04':
        month = 'Apr';
        break;
      case '05':
        month = 'May';
        break;
      case '06':
        month = 'Jun';
        break;
      case '07':
        month = 'Jul';
        break;
      case '08':
        month = 'Aug';
        break;
      case '09':
        month = 'Sep';
        break;
      case '10':
        month = 'Oct';
        break;
      case '11':
        month = 'Nov';
        break;
      case '12':
        month = 'Dec';
        break;

    }

    date = month + ' ' + year;
    return date;
  }

  var permitTypes = JSON.parse($("#permitstype")[0].childNodes[0].data),      cleanPermitData = [],
      cleanPermitLabels = [];

  //set the data up for Charts.js
  for(var i = 0; i < permitTypes.data.length; i+=1) {

    if(permitTypes.data[i].permit_type != 'CCUT') {

      cleanPermitLabels.push(humanNames(permitTypes.data[i].permit_type));
      cleanPermitData.push(permitTypes.data[i].count);
      //console.log(data[i].issue_type, i);

    }

  }

  var vdata2 = {
    labels: cleanPermitLabels,
    datasets: [
      {
        label: "Permits by Type",
        fillColor: t_purple_1,
        strokeColor: purple_1,
        data: cleanPermitData
      }
    ]
  };

  function humanNames(type) {

    //console.log(type);

    switch(type) {

      case 'FIRE':

        return 'Fire';
        break;

      case 'MMEC':

        return 'Municipal: Mechanical';
        break;

      case 'ZIPS':

        return 'Zoning Improvement Permit';
        break;

      case 'MELE':

        return 'Muncipal: Electrical';
        break;

      case 'CCUT':

        return 'CCUT';
        break;

      case 'ELEC':

        return 'Electrical';
        break;

      case 'PLUM':

        return 'Plumbing';
        break;

      case 'MPLU':

        return 'Municipal: Plumbing';
        break;

      case 'MBLD':

        return 'Municipal: Building';
        break;

      case 'LPGX':

        return 'Liquid Petroleum Gas';
        break;

      case 'BLDG':

        return 'Building';
        break;

      case 'MECH':

        return 'Mechanical';
        break;

    }

  }

  $('#permitTypeChart').parent().parent().find('.headline').html(permitTypes.title);      
        
  /************************* LEAFLET MAPPING *************************/

  //25.7667° N, 80.2000° W
  //{lat: 25.626668871238568, lng: -80.44867515563963}

  var map = L.map('leaflet').setView([25.626668871238568, -80.44867515563963], 10);
    L.tileLayer('//api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    minZoom: 9,
    id: 'phiden.e64a2341',
    accessToken: 'pk.eyJ1IjoicGhpZGVuIiwiYSI6ImM3MGIxMDA2MDA1NDkzMzY5MWNlZThlYzFlNWQzOTkzIn0.boD45w3d4Ajws7QFysWq8g'
    }).addTo(map);

  //county shapefiles
  $.ajax({
    type: "GET",
    url: "../static/geodata/municipalities_coast.json",
    dataType: "json",
    success: parseXML
  });

  function parseXML(data) {

    var muni = [],
        umsa = [],
        i,
        myStyle = {
          color: green,
          weight: 1,
          opacity: 0.65
        },

        umsaStyle = {

          color: 'rgba(0,0,0)',
          weight: 1,
          opacity: 0.65

        };

    //sort for county to control style
    for(i = 0; i < data.features.length;   i+=1) {

      if(data.features[i].properties.NAME == 'UNINCORPORATED MIAMI-DADE') {

        umsa.push(data.features[i]);

      } else {

        muni.push(data.features[i]);

      }

    }

    L.geoJson(muni, {style:umsaStyle}).addTo(map);
    L.geoJson(umsa, {style:myStyle}).addTo(map);

    buildDataMaps();

  }
  
  function getRandomArbitrary(min, max) {
    return Math.round(Math.random() * (max - min) + min);
  }

  
  function buildDataMaps(){
    
    var vioLocationsData = JSON.parse($("#violations_locations_json")[0].childNodes[0].data),
        vioTypeData = JSON.parse($("#violations_type_json")[0].childNodes[0].data),
        vioMonthlyData = JSON.parse($("#violations_per_month_json")[0].childNodes[0].data),
        vioArray = [];
        
    for(i = 0; i < vioLocationsData.length; i+=1) {

      if(vioLocationsData[i].location.latitude != undefined) {
        
        var obj = vioLocationsData[i].location.human_address;
        //console.log(typeof obj);
        //console.log(obj.split(":")[obj.split(":").length - 1])
        
       // var latlng = L.latLng(vioLocationsData[i].location.latitude, vioLocationsData[i].location.longitude, 1);
        
        vioArray[i] = [parseFloat(vioLocationsData[i].location.latitude), parseFloat(vioLocationsData[i].location.longitude)];

        /*var lat = vioLocationsData[i].location.latitude,
            lon = vioLocationsData[i].location.longitude,
            openClosed = vioLocationsData[i].ticket_status,
            fill = t_yellow,
            color = yellow,
            title = vioLocationsData[i].issue_type;

        var marker2 = L.circleMarker([lat, lon], {
            radius: 5,
            fillColor: fill,
            color: color,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map);

          marker2.bindPopup(title);
          marker2.on('mouseover', function() {
            this.openPopup();
          });
          marker2.on('mouseout', function() {
            this.closePopup();
          });*/
      }
    }
    
    console.log(vioArray.length);
    
    var heat = L.heatLayer(vioArray).addTo(map);
    
        console.log(map.hasLayer(heat), heat);
        
    
    for(i = 0; i < vioMonthlyData.length; i += 1) {

      //console.log(vioMonthlyData[i]);

      /*if(vioMonthlyData[i].location.latitude != undefined) {

        lat = vioMonthlyData[i].location.latitude,
        lon = vioMonthlyData[i].location.longitude,
        openClosed = vioMonthlyData[i].ticket_status,
        fill = t_yellow,
        color = yellow,
        title = vioMonthlyData[i].issue_type;

        marker2 = L.circleMarker([lat, lon], {
          radius: 5,
          fillColor: fill,
          color: color,
          weight: 1,
          opacity: 1,
          fillOpacity: 0.8
        }).addTo(map3);

        marker2.bindPopup(title);
        marker2.on('mouseover', function() {
          this.openPopup();
        });
        marker2.on('mouseout', function() {
          this.closePopup();
        });

      }*/


    }

    if(vioTypeData === '') {

      $('#regulation h3').append("<div class='alert-alert-warning'><p class='alert center small'>Sorry, something's gone wrong with our data for neighborhood compliance! <br>We're working to get it back online.</p></div>");

    } else {

      var labels = [];
      var dataset = [];

      //the 'total' isn't an integer. make it one, or the sort will fail.
      for(i = 0; i < vioTypeData.length;   i+=1) {

        vioTypeData[i].total = parseInt(vioTypeData[i].total, 10);
        //console.log(data[i]);
      }

      //sort on the number of each violation type
      vioTypeData = vioTypeData.sortOn("total");
      vioTypeData.reverse();

      //set the data up for Charts.js
      for(i = 0; i < 19;   i+=1) {

        labels[i] = vioTypeData[i].issue_type;
        dataset[i] = vioTypeData[i].total;
        //console.log(data[i].issue_type, i);

      }

      labels.reverse();
      dataset.reverse();

      //create the chart
      var bctx = $("#viotype").get(0).getContext("2d");

      var bdata = {
          labels: labels,
          datasets: [
              {
                fillColor: t_purple_1,
                strokeColor: purple_1,
                data: dataset
              }
          ]
      };

      var horizontalBarChart = new Chart(bctx).HorizontalBar(bdata);

    }

  }

  Array.prototype.sortOn = function(){
    var dup = this.slice();
    if(!arguments.length) return dup.sort();
    var args = Array.prototype.slice.call(arguments);
    return dup.sort(function(a,b){
      var props = args.slice();
      var prop = props.shift();
      while(a[prop] == b[prop] && props.length) prop = props.shift();
      return a[prop] == b[prop] ? 0 : a[prop] > b[prop] ? 1 : -1;
    });
  };

 

  /***************************** tool tips *****************************/

  /******** Documentation from Google sheets, using Tabletop.js **********/

  var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/170neJyhcBkg3sgABsqKk1B6WJa51r6oo6PEMAlwOBB8/pubhtml';

  function initTabletop(){
    Tabletop.init( { key: public_spreadsheet_url,
                     callback: buildTipsy,
                     simpleSheet: true,
                     prettyColumnNames: false } );
  }

  var tableData = [];

  function buildTipsy(data) {
    //alert("Successfully processed!")
    console.log(data);

    for(var i = 0; i < data.length; i+=1) {

      var obj = {};

        obj.hID = data[i].hoverid;
        obj.text = data[i].descriptionforhover;

      tableData.push(obj);

    }

    $('.tooltip').each(function() {

      var id = $(this).attr('id');

      for(var i = 0; i < data.length; i+=1) {

        if(id == data[i].hoverid) {
          
          console.log(data[i].hoverid)
          $(this).attr('title', data[i].descriptionforhover);
          var mid = '#' + data[i].hoverid;
          $(mid).append(data[i].descriptionforhover);
          
        }
      }
    });
  }

  initTabletop();

}); //close ready
