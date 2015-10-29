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

  //surveys by role
  var sctx = $("#s-role-chart").get(0).getContext("2d"),
      sctxdata = JSON.parse($("#surveyrole")[0].childNodes[0].data),
      sctxseries = [],
      sctxlabels = [],

      //this only works because it's a known quantity.
      homeowners = {label:'Homeowners', count:0},
      architects = {label:'Architects', count:0},
      contractors = {label:'Contractors', count:0},
      consultants = {label:'Permit Consultants', count:0},
      owners = {label:'Business Owners', count:0},
      sorter = [architects, owners, consultants, contractors, homeowners],
      i,
      respondentsByRole,
      respondentsByRoleChart;



  for(i = 0; i < sctxdata.data.length; i+=1) {

    switch(parseInt(sctxdata.data[i][0], 10)) {

      case 1:
        contractors.count = sctxdata.data[i][1];
        break;
      case 2:
        architects.count = sctxdata.data[i][1];
        break;
      case 3:
        consultants.count = sctxdata.data[i][1];
        break;
      case 4:
        homeowners.count = sctxdata.data[i][1];
        break;
      case 5:
        owners.count = sctxdata.data[i][1];
        break;

    }

  }

  for(i = 0; i < sorter.length; i+=1) {

    sctxseries[i] = sorter[i].count;
    sctxlabels[i] = sorter[i].label;

  }

  respondentsByRole = {
    labels: sctxlabels,
    datasets: [
        {
            label: "Respondents by Role",
            fillColor: t_purple_1,
            strokeColor: purple_1,
            data: sctxseries
        }
    ]
  };

  respondentsByRoleChart = new Chart(sctx).HorizontalBar(respondentsByRole);

  // end surveys by role

  // successful task completion
  var cctx = $("#s-complete-chart").get(0).getContext("2d"),
      cctxdata = JSON.parse($("#surveycomplete")[0].childNodes[0].data),
      total = cctxdata.data.total,
      completeTrue = cctxdata.data.yes,
      completeFalse = total - completeTrue,

    cctxPie = [
    {
      value: completeTrue,
      color:purple_1,
      highlight: t_purple_1,
      label: 'Successfully completed task'
    },
    {
      value: completeFalse,
      color: purple_4,
      highlight: t_purple_4,
      label: 'Failed to complete task'
    }
  ],

  cctxPieChart = new Chart(cctx).Pie(cctxPie),
  // end successful task completion

  // surveys by purpose
  sptx = $("#s-purpose-chart").get(0).getContext("2d"),
  sptxdata = JSON.parse($("#surveypurpose")[0].childNodes[0].data),

  //this only works because it's a known quantity.
  violation = {label:'Find out about a violation/lien', count:0},
  inspector = {label:'Meet with an inspector', count:0},
  permit = {label:'Apply for a permit', count:0},
  reviewer = {label:'Meet with a plan reviewer', count:0},
  cu = {label:'Obtain a certificate of use/occupancy', count:0},
  other = {label:'Other', count:0},
  sorter2 = [violation, inspector, permit, reviewer, cu, other],

  sptxseries = [],
  sptxlabels = [],
  surveysByPurpose,
  surveysByPurposeChart;

  var test = 0;

  for(i = 0; i < sptxdata.data.length; i+=1) {

    switch(parseInt(sptxdata.data[i][0], 10)) {

      case 1:
        permit.count += sptxdata.data[i][1];
        break;
      case 2:
        inspector.count += sptxdata.data[i][1];
        break;
      case 3:
        reviewer.count += sptxdata.data[i][1];
        break;
      case 4:
        violation.count += sptxdata.data[i][1];
        break;
      case 5:
        cu.count += sptxdata.data[i][1];
        break;
      case 6:
        other.count += sptxdata.data[i][1];
      default:
        other.count += 1;

    }

  }

  for(i = 0; i < sorter2.length; i+=1) {
    sptxseries[i] = sorter2[i].count;
    sptxlabels[i] = sorter2[i].label;
  }

  surveysByPurpose = {
    labels: sptxlabels,
    datasets: [
      {
        label: "Respondents by Purpose",
        fillColor: t_purple_1,
        strokeColor: purple_1,
        data: sptxseries
      }
    ]
  };

  surveysByPurposeChart = new Chart(sptx).HorizontalBar(surveysByPurpose);
  // end surveys by purpose
  
  // Get context with jQuery - using jQuery's .get() method.
  var ctx = $("#myChart").get(0).getContext("2d"),
      jsondata = JSON.parse($("#jsondata")[0].childNodes[0].data),
      series = jsondata.series[0].data,
      datetime = jsondata.datetime.data,

      data = {
        labels: datetime,
        scaleBeginAtZero: true,
        datasets: [
            {
                label: "My First dataset",
                fillColor: t_orange,
                strokeColor: orange,
                pointColor: orange,
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: series,
                scaleStartValue: 0
            }
        ]
      },

      myPieChart,
      myLineChart = new Chart(ctx).Line(data),
      surveyData = JSON.parse($("#surveydata")[0].childNodes[0].data),
      pctx = $("#surveyChart").get(0).getContext("2d"),

      pieData = [
        {
          value: surveyData.data.web_en,
          color:purple_1,
          highlight: t_purple_1,
          label: surveyData.labels.web_en
        },
        {
          value: surveyData.data.web_es,
          color: purple_2,
          highlight: t_purple_2,
          label: surveyData.labels.web_es
        },
        {
          value: surveyData.data.sms_en,
          color: purple_3,
          highlight: t_purple_3,
          label: surveyData.labels.sms_en
        },
        {
          value: surveyData.data.sms_es,
          color: purple_4,
          highlight: t_purple_4,
          label: surveyData.labels.sms_es

        }
      ];

      $('#surveyChart').parent().parent().find('.headline').html(surveyData.title);
      myPieChart = new Chart(pctx).Pie(pieData);

  /* Permitting & violations */

  var ctx2 = $("#openPermits").get(0).getContext("2d"),
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

  buildOpenPermitChart();
  buildViolationsCharts();

  function buildOpenPermitChart() {

    for(i = 0; i < permitJSON.length; i++) {

      series2.push(permitJSON[i].total);
      datetime2.push(prettyDates((permitJSON[i].month).split('T')[0]));

    }

    series2.reverse();
    datetime2.reverse();

    openPermitDataset = {
        labels:datetime2,
        datasets: [
          {
              fillColor: t_orange,
              strokeColor: orange,
              pointColor: orange,
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: series2
          }
        ]
    },

    openPermitChart = new Chart(ctx2).Line(openPermitDataset);

  }

  function buildViolationsCharts() {

    for(i = 0; i < violationsJSON.length; i++) {

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

  var permitTypes = JSON.parse($("#permitstype")[0].childNodes[0].data),
      pttx = $("#permitTypeChart").get(0).getContext("2d"),
      cleanPermitData = [],
      cleanPermitLabels = [];

  //set the data up for Charts.js
  for(i = 0; i < permitTypes.data.length; i+=1) {

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
  var barChart2 = new Chart(pttx).HorizontalBar(vdata2),
  
      plumbingChart = $("#p-plumbing").get(0).getContext("2d"),
      buildingChart = $("#p-building").get(0).getContext("2d"),
      fireChart = $("#p-fire").get(0).getContext("2d"),
      elexChart = $("#p-electrical").get(0).getContext("2d"),
      zoningChart = $("#p-zoning").get(0).getContext("2d"),
      pData = parseInt($('#plumbing-data').text()),
      bData = parseInt($('#building-data').text()),
      fData = parseInt($('#fire-data').text()),
      eData = parseInt($('#electrical-data').text()),
      zData = parseInt($('#zoning-data').text()),
      
      plumbingData = [
        {
          value: pData,
          color:purple_1,
          highlight: t_purple_1,
          label: 'Plumbing: same-day'
        },
        {
          value: (100 - pData),
          color: purple_2,
          highlight: t_purple_2,
          label: 'Plumbing'
        }
      ],
      
      buildingData = [
        {
          value: bData,
          color:purple_1,
          highlight: t_purple_1,
          label: 'Building: same-day'
        },
        {
          value: (100 - bData),
          color: purple_2,
          highlight: t_purple_2,
          label: 'Building'
        }
      ],
      
      fireData = [
        {
          value: fData,
          color:purple_1,
          highlight: t_purple_1,
          label: 'Fire: same-day'
        },
        {
          value: (100 - fData),
          color: purple_2,
          highlight: t_purple_2,
          label: 'Fire'
        }
      ],
      
      elexData = [
        {
          value: eData,
          color:purple_1,
          highlight: t_purple_1,
          label: 'Electrical: same-day'
        },
        {
          value: (100 - eData),
          color: purple_2,
          highlight: t_purple_2,
          label: 'Electrical'
        }
      ],
      
      zoningData = [
        {
          value: zData,
          color:purple_1,
          highlight: t_purple_1,
          label: 'Zoning: same-day'
        },
        {
          value: (100 - zData),
          color: purple_2,
          highlight: t_purple_2,
          label: 'Zoning'
        }
      ],
      
      pChart = new Chart(plumbingChart).Pie(plumbingData),
      bChart = new Chart(buildingChart).Pie(buildingData),
      fChart = new Chart(fireChart).Pie(fireData),
      eChart = new Chart(elexChart).Pie(elexData),
      zChart = new Chart(zoningChart).Pie(zoningData);
      
        
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
        //console.log(obj);
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
        
        map.addLayer(heat);
    
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

  /***************************** star ratings *****************************/

  $('#star-rating').raty({
    score: function() {
      //console.log($(this).find('.hidden').text(), 'is value')
      return $(this).find('.invisible').text();
      },
      path: 'static/images',
      half: true,
      readOnly:true,
      number:7
    });

    $('#s-lang-rate-en').raty({
    score: function() {
      //console.log($(this).find('.hidden').text(), 'is value')
      return $('#rate-en').text();
      },
      path: 'static/images',
      half: true,
      readOnly:true,
      number:7
    });

    $('#s-lang-rate-es').raty({
      score: function() {
        return $('#rate-en').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-permit').raty({
      score: function() {
        return $('#rate-permit').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-inspect').raty({
      score: function() {
        return $('#rate-inspect').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-review').raty({
      score: function() {
        return $('#rate-review').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-liens').raty({
      score: function() {
        return $('#rate-liens').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-cu').raty({
      score: function() {
        return $('#rate-cu').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-permit').raty({
      score: function() {
        return $('#role-rate-permit').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-cu').raty({
      score: function() {
        return $('#role-rate-cu').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-inspect').raty({
      score: function() {
        return $('#role-rate-inspect').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-review').raty({
      score: function() {
        return $('#role-rate-review').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-lien').raty({
      score: function() {
        return $('#role-rate-lien').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });



  //}

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
    //console.log(data);

    for(var i = 0; i < data.length;   i+=1) {

      var obj = {};

        obj.hID = data[i].hoverid;
        obj.text = data[i].descriptionforhover;

      tableData.push(obj);

    }

    $('.tipsy-hook').each(function() {

      var id = $(this).attr('id');
      //console.log(id);

      for(var i = 0; i < data.length;   i+=1) {

        if(id == data[i].hoverid) {

          $(this).attr('title', data[i].descriptionforhover);
          var mid = '#' + data[i].hoverid;
          $(mid).tipsy();
          //console.log(mid);
        }
      }
    });
  }

  initTabletop();

}); //close ready
