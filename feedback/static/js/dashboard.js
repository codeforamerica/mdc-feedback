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
	
	console.log(apiModal);
	
	if(apiModal != undefined) {
		
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

			var offset = 300 - h - details.height() * 2 - 26;	//300 is fixed height, 20 is padding
			//console.log(offset);

			$(container).css('height', offset);


		}

		$(details).removeClass("invisible-button");

	})

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
	
	var red = 'rgba(0,0,0,1)';
	var t_red = 'rgba(1,1,1,1)';
	
	var b = 'rgba(2,2,2,1)';
	var t_b = 'rgba(3,3,3,1)';
	

	var colors = [green, yellow, orange, purple, purple_1, purple_2, purple_3, purple_4, red, b];
	var t_colors = [t_green, t_yellow, t_orange, t_purple, t_purple_1, t_purple_2, t_purple_3, t_purple_4, red, t_b];

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

	var	pctx = $("#surveyChart").get(0).getContext("2d");

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
	]

	$('#surveyChart').parent().parent().find('.headline').html(surveyData.title);
	var myPieChart = new Chart(pctx).Pie(pieData);/**/

	/* Permitting */

		$.ajax({
		  url: "https://opendata.miamidade.gov/resource/awsz-tanw.json?$select=date_trunc_ym(issuedate)%20AS%20month,%20count(*)%20AS%20total&$group=month&$order=month%20desc&$limit=12&$offset=2",

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
			            pointHighlightStroke: "rgba(220,220,220,1)",
			            data: series

			        }

			    ]
			};

			var myLineChart = new Chart(ctx2).Line(d);

		});
		
		console.log(JSON.parse($("#permitstype")[0].childNodes[0].data));
		var permitTypes = JSON.parse($("#permitstype")[0].childNodes[0].data);
		
		var	pttx = $("#permitTypeChart").get(0).getContext("2d");
		
		var cleanPermitData = [];
		
		for(var i = 0; i < permitTypes.data.length; i++) {
		
			var obj = {};
				obj.value = permitTypes.data[i].count;
				obj.color = colors[i];
				obj.highlight = t_colors[i];
				obj.label = permitTypes.data[i].permit_type;
				
			console.log(obj.label);
			
			cleanPermitData.push(obj);
		}

		$('#permitTypeChart').parent().parent().find('.headline').html(permitTypes.title);
		var myPieChart2 = new Chart(pttx).Pie(cleanPermitData);

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
	var map = L.map('leaflet').setView([25.7667, -80.2000], 10);
	L.tileLayer('//api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    minZoom: 10,
    id: 'phiden.e64a2341',
    accessToken: 'pk.eyJ1IjoicGhpZGVuIiwiYSI6ImM3MGIxMDA2MDA1NDkzMzY5MWNlZThlYzFlNWQzOTkzIn0.boD45w3d4Ajws7QFysWq8g'		     
    }).addTo(map);

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

				var marker = L.circleMarker([lat, lon], {
		        radius: 5,
		        fillColor: fill,
		        color: color,
		        weight: 1,
		        opacity: 1,
		        fillOpacity: 0.8
		    }).addTo(map);

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

			var horizontalBarChart = new Chart(bctx).HorizontalBar(bdata	);

		})

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

}) //close ready
