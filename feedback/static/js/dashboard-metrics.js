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

  var ctx2 = $("#openPermits").get(0).getContext("2d"),
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
  
  function buildOpenPermitChart() {

    for(var i = 0; i < permitJSON.length; i++) {

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
