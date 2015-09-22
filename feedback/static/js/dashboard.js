$(document).ready(function() {

  /* API HEALTH CHECK */
  window.REMODAL_GLOBALS = {
    NAMESPACE: 'modal',
    DEFAULTS: {
      hashTracking: false
    }
  };

  var apiStatus = parseInt($('#api-health').text());
  var apiModal = $('[data-remodal-id=modal]').remodal();

  //console.log(apiModal);

  if(apiModal !== undefined) {

    if(apiStatus === -1) {

    //county error.
    $('.remodal').find('#status').text("Uhoh, something went wrong!");
    $('.remodal').find('p').text("It looks like we've had a problem with our data. Check back later for an update.");
    apiModal.open();


    } else if(apiStatus === 1) {

      //mostly so I can test the modals
      $('.remodal').find('#status').text("All is well.");
      //apiModal.open();

    } else {

      //http error code.
      $('.remodal').find('#status').text("Uhoh, something went wrong!");
      $('.remodal').find('p').text("It looks like our Socrata link is down (error" + apiStatus + "). Check back later for an update.");
      apiModal.open();

    }

  }

  //console.log(apiStatus)

  /************************* dashboard css *************************/

  $('.headline').each(function() {

    var h = $(this).height();
    var container = $(this).parent().find('.content-container');
    var details = $(this).parent().find('.details');

    //console.log('headline is ', h, details.height() )
    //a single line of text is 25px high.
    //if we have a 2x tall headline, need to reposition .details
    //we do this by adjusting .content-container height
    if(h > 25) {

      var offset = 300 - h - details.height() * 2 - 26;  //300 is fixed height, 20 is padding
      //console.log(offset);

      $(container).css('height', offset);


    }

    $(details).removeClass("invisible-button");

  });

  /***************************** CHARTS! *****************************/

  var green = "rgba(76, 216, 132, 1)";
  var t_green = "rgba(76, 216, 132, 0.2)";

  var yellow = "rgba(245, 201, 61, 1)";
  var t_yellow = "rgba(245, 201, 61, 0.2)";

  var orange = "rgba(243, 155, 121, 1)";
  var t_orange = "rgba(243, 155, 121, 0.2)";

  var purple = "rgba(61, 51, 119, 1)";
  var t_purple = "rgba(61, 51, 119, 0.2)";

  var purple_1 = 'rgba(172, 75, 173, 1)';
  var t_purple_1 = 'rgba(172, 75, 173, 0.2)';

  var purple_2 = 'rgba(122, 0, 134, 1)';
  var t_purple_2 = 'rgba(122, 0, 134, 0.2))';

  var purple_3 = 'rgba(75, 0, 94, 1)';
  var t_purple_3 = 'rgba(75, 0, 94, 0.2)';

  var purple_4 = 'rgba(219, 172, 217, 1)';
  var t_purple_4 = 'rgba(219, 172, 217, 0.2)';

  var blue = 'rgba(93, 205, 252,1)';
  var t_blue = 'rgba(93, 205, 252, 0.2)';

  var b = 'rgba(170, 233, 254,1)';
  var t_b = 'rgba(170, 233, 254,.2)';


  var colors = [green, yellow, orange, purple, purple_1, purple_2, purple_3, purple_4, blue, b];
  var t_colors = [t_green, t_yellow, t_orange, t_purple, t_purple_1, t_purple_2, t_purple_3, t_purple_4, t_blue, t_b];

  var pie_colors = ['rgba(64, 0, 76, 1)', 'rgba(118, 42, 131,1)', 'rgba(153, 112, 171, 1)', 'rgba(194, 165, 207, 1)', 'rgba(231, 212, 232, 1)', 'rgba(217 240 211, 1)', 'rgba(166, 219, 160, 1)', 'rgba(90, 174, 97, 1)', 'rgba(27, 120, 55, 1)', 'rgba(0, 68, 27, 1)', b, blue]

  Chart.defaults.global = {
    // Boolean - Whether to animate the chart
    animation: true,

    // Number - Number of animation steps
    animationSteps: 60,

    animationEasing: "easeOutQuart",

    // Boolean - If we should show the scale at all
    showScale: true,

    // Boolean - If we want to override with a hard coded scale
    scaleOverride: false,

    // ** Required if scaleOverride is true **
    // Number - The number of steps in a hard coded scale
    scaleSteps: null,
    // Number - The value jump in the hard coded scale
    scaleStepWidth: null,
    // Number - The scale starting value
    scaleStartValue: null,

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
    onAnimationProgress: function(){},

    // Function - Will fire on animation completion.
    onAnimationComplete: function(){}
}

  if($("#dashboard")[0] != undefined) {

  // Get context with jQuery - using jQuery's .get() method.
  var ctx = $("#myChart").get(0).getContext("2d");

  var jsondata = JSON.parse($("#jsondata")[0].childNodes[0].data);
  //console.log(jsondata);

  var series = jsondata.series[0].data;
  var datetime = jsondata.datetime.data;
  //console.log(series, datetime);

  var data = {
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
  };

  var myLineChart = new Chart(ctx).Line(data);
  var surveyData = JSON.parse($("#surveydata")[0].childNodes[0].data);

  //console.log(surveyData);

  var  pctx = $("#surveyChart").get(0).getContext("2d");

  var pieData = [
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
  var myPieChart = new Chart(pctx).Pie(pieData);/**/

  /* Permitting */

    $.ajax({
      url: "https://opendata.miamidade.gov/resource/vvjq-pfmc.json?$select=date_trunc_ym(permit_issued_date)%20AS%20month,count(*)%20AS%20total&$group=month&$order=month%20desc&$limit=12&$where=starts_with(process_number,%27C%27)&master_permit_number=0&permit_type=%27BLDG%27&$offset=1",
      context: document.body
    }).done(function(data) {

      var ctx2 = $("#openPermits").get(0).getContext("2d");
      //console.log(data);

      var series = [];
      var datetime = [];

      for(var i = 0; i < data.length; i++) {

        datetime.push(data[i].month.split('-')[1] + '/' + data[i].month.split('-')[0]);
        series.push(data[i].total);

      }

      //socrata pushes the data backwards. fix that.
      datetime.reverse();
      series.reverse();

      var d = {
          labels:datetime,
          datasets: [
            {
                fillColor: t_orange,
                strokeColor: orange,
                pointColor: orange,
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: series
            }
          ]
      };

      var myLineChart = new Chart(ctx2).Line(d);

    });

    //console.log(JSON.parse($("#permitstype")[0].childNodes[0].data));
    var permitTypes = JSON.parse($("#permitstype")[0].childNodes[0].data);

    var pttx = $("#permitTypeChart").get(0).getContext("2d");

    var cleanPermitData = [];
    var cleanPermitLabels = [];
    
    //set the data up for Charts.js
    for(var i = 0; i < permitTypes.data.length; i++) {

      cleanPermitLabels[i] = permitTypes.data[i].permit_type;
      cleanPermitData[i] = permitTypes.data[i].count;
      //console.log(data[i].issue_type, i);

    }
    
    var vdata = {
      labels: cleanPermitLabels,
      datasets: [
          {
              label: "Permits by Type",

              fillColor: t_purple_1,
              strokeColor: purple_1,
              data: cleanPermitData
          },

      ]
    };

    $('#permitTypeChart').parent().parent().find('.headline').html(permitTypes.title);
    var barChart2 = new Chart(pttx).Bar(vdata);
   
  /* VIOLATIONS */

  $.ajax({
      url: "https://opendata.miamidade.gov/resource/tzia-umkx.json?$select=date_trunc_ym(ticket_created_date_time)%20AS%20month,%20count(*)%20AS%20total&$group=month&$order=month%20desc&$limit=12&$offset=1",
      context: document.body
    }).done(function(data) {

      var ctx3 = $("#violations").get(0).getContext("2d");
      //console.log(data);

      var series = [];
      var datetime = [];

      for(var i = 0; i < data.length; i++) {

        datetime.push(data[i].month.split('-')[1] + '/' + data[i].month.split('-')[0]);
        series.push(data[i].total);

      }

      //socrata pushes the data backwards. fix that.
      datetime.reverse();
      series.reverse();

      var d3 = {
        labels:datetime,
        datasets: [
          {
            label: "My First dataset",
            scaleOverride: true,
            scaleSteps: 50,
            scaleStepWidth: 200,
            scaleBeginAtZero:true,
            scaleStartValue:0,
            fillColor: t_orange,
            strokeColor: orange,
            pointColor: orange,
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: purple,
            data: series
          }
        ]
      };

      var myLineChart = new Chart(ctx3).Line(d3);

    });

  /************************* LEAFLET MAPPING *************************/

  //25.7667° N, 80.2000° W
  //{lat: 25.626668871238568, lng: -80.44867515563963}

  var map = L.map('leaflet').setView([25.626668871238568, -80.44867515563963], 9);
    L.tileLayer('//api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    minZoom: 9,
    id: 'phiden.e64a2341',
    accessToken: 'pk.eyJ1IjoicGhpZGVuIiwiYSI6ImM3MGIxMDA2MDA1NDkzMzY5MWNlZThlYzFlNWQzOTkzIn0.boD45w3d4Ajws7QFysWq8g'
    }).addTo(map);

  var map2 = L.map('leaflet-open').setView([25.626668871238568, -80.44867515563963], 9);
    L.tileLayer('//api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    minZoom: 9,
    id: 'phiden.e64a2341',
    accessToken: 'pk.eyJ1IjoicGhpZGVuIiwiYSI6ImM3MGIxMDA2MDA1NDkzMzY5MWNlZThlYzFlNWQzOTkzIn0.boD45w3d4Ajws7QFysWq8g'
    }).addTo(map2);

  var map3 = L.map('leaflet-lein').setView([25.626668871238568, -80.44867515563963], 9);
    L.tileLayer('//api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    minZoom: 9,
    id: 'phiden.e64a2341',
    accessToken: 'pk.eyJ1IjoicGhpZGVuIiwiYSI6ImM3MGIxMDA2MDA1NDkzMzY5MWNlZThlYzFlNWQzOTkzIn0.boD45w3d4Ajws7QFysWq8g'
    }).addTo(map3);

    map3.on('click', function(e) {
      // console.log(e.latlng);
    });

  //county shapefiles
  $.ajax({
    type: "GET",
    url: "../static/geodata/municipalities_coast.json",
    dataType: "json",
    success: parseXML,
    error: logError
  });


  function logError(n, textStatus, errorThrown) {

    alert("ajax shapefile error", textStatus, errorThrown);
  }

  function parseXML(data) {

   var muni = [];
   var umsa = [];

    //sort for county to control style
    for(var i = 0; i < data.features.length; i++) {

	    if(data.features[i].properties.NAME == 'UNINCORPORATED MIAMI-DADE') {

		    umsa.push(data.features[i]);

	    } else {

		    muni.push(data.features[i]);

	    }

    }

    var myStyle = {
      "color": blue,
      "weight": 1,
      "opacity": 0.65
    };

    var umsaStyle = {

	    "color": 'rgba(0,0,0)',
      "weight": 1,
      "opacity": 0.65

    }

    L.geoJson(muni, {style:umsaStyle}).addTo(map);
    L.geoJson(umsa, {style:myStyle}).addTo(map);
    L.geoJson(muni, {style:umsaStyle}).addTo(map2);
    L.geoJson(umsa, {style:myStyle}).addTo(map2);
    L.geoJson(muni, {style:umsaStyle}).addTo(map3);
    L.geoJson(umsa, {style:myStyle}).addTo(map3);

    //data map
  $.ajax({
      url: "https://opendata.miamidade.gov/resource/tzia-umkx.json?$where=ticket_created_date_time%20%3E%20%272015-01-01%27",

      context: document.body
    }).done(function(data) {

      for(var i = 0; i < data.length; i++) {

        var lat = data[i].location.latitude;
        var lon = data[i].location.longitude;
        var openClosed = data[i].ticket_status;
        var fill = t_yellow;
        var color = yellow;
        var title = data[i].issue_type;

        //console.log(openClosed);

        if(openClosed == 'LOCKED') {
          var marker = L.circleMarker([lat, lon], {
            radius: 5,
            fillColor: t_green,
            color: green,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map2);

        }

        if(openClosed == "LIEN") {
          var marker = L.circleMarker([lat, lon], {
            radius: 5,
            fillColor: t_purple,
            color: purple,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map3);
        }

        if(openClosed == "CLOSED") {

          var marker = L.circleMarker([lat, lon], {
            radius: 5,
            fillColor: fill,
            color: color,
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
          }).addTo(map);

        }

        marker.bindPopup(title);
        marker.on('mouseover', function (e) {
            this.openPopup();
        });
        marker.on('mouseout', function (e) {
            this.closePopup();
        });
      }

    })

    $.ajax({
      url: "https://opendata.miamidade.gov/resource/dj6j-qg5t.json?&case_owner=Regulatory_and_Economic_Resources&$select=issue_type,%20count(*)%20AS%20total&$group=issue_type&$where=ticket_created_date_time%20%3E=%20%272015-01-11%27",

      context: document.body

    }).done(function(data) {

      //console.log('data: ', data);

      var labels = [];
      var dataset = [];

      //the 'total' isn't an integer. make it one, or the sort will fail.
      for(var i = 0; i < data.length; i++) {

        data[i].total = parseInt(data[i].total);

      }

      //sort on the number of each violation type
      data = data.sortOn("total");
      data.reverse();

      //set the data up for Charts.js
      for(var i = 0; i < 19; i++) {

        labels[i] = data[i].issue_type;
        dataset[i] = data[i].total;
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
                  label: "My First dataset",

                  fillColor: t_purple_1,
                  strokeColor: purple_1,
                  data: dataset
              },

          ]
      };

      var horizontalBarChart = new Chart(bctx).HorizontalBar(bdata);

    });

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

  }

  /***************************** tag clouds *****************************/

  //sanitize array
  var blacklist = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',  'your',
    'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she',
    'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their',
    'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had',  'having', 'do', 'does', 'did', 'doing', 'a', 'an',
    'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of',
    'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then',
    'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
    'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', 'should', 'now', 'id', 'var', 'function', 'js', 'd',
    'script', '\'script', 'fjs', 'document'];

  var temp = [];

  function sanitize(array, container, hide) {

     for(var i = 0; i < blacklist.length; i++) {

        var result = array.filter(function(elem){

          if(elem.length > 1) {

            return elem.toLowerCase() != blacklist[i];
          }

        })

        array = result;
        //console.log(result);
      }

      //count the words remaining after sanitation
    var newObject = {};
    $.each(array, function (ix, val) {
        if (newObject[val]) {
            newObject[val]++;
        }
        else {
            //console.log('that wasnt in the array', val);
            newObject[val] = 1;
        }
    });

    var temp = []; //storage array

    //format for jQCloud
    $.each(newObject, function(key, value) {

      var obj = { "text" : key, "weight": value};
      temp.push(obj);

    })

    array = temp; //reassign
    //console.log(array);

    continueCloud(array, container, hide);
  }

  //called by sanitize
  function continueCloud(array, container, hide) {

    $(container).jQCloud(array, {shape: 'rectangular', height:200, autoResize: true});
    $(hide).each(function() { $(this).addClass('hidden');})
  }

  //best & worst
  var words = $('#bestworst-data').text();
  var wordArray = words.split(' ');
  sanitize(wordArray, '#bestworst-data', '#bestworst-data p');

  //suggested improvements
  var suggests = $('#improvements-data').text();
  var suggestArray = suggests.split(' ');
  sanitize(suggestArray, '#improvements-data', '#improvements-data p');

  //more comments
  var comments = $('#morecomments-data').text();
  var commentsArray = comments.split(' ');
  sanitize(commentsArray, '#morecomments-data', '#morecomments-data p');

	/***************************** tool tips *****************************/

	$('#test').tipsy();

}); //close ready
