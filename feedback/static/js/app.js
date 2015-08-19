$(document).ready(function() {

	/************************* dashboard css *************************/

	$('.headline').each(function() {

		var h = $(this).height();
		var container = $(this).parent().find('.content-container');
		var details = $(this).parent().find('.details');

		console.log('headline is ', h, details.height() )
		//a single line of text is 25px high.
		//if we have a 2x tall headline, need to reposition .details
		//we do this by adjusting .content-container height
		if(h > 25) {

			var offset = 300 - h - details.height() * 2 - 26;	//300 is fixed height, 20 is padding
			console.log(offset);

			$(container).css('height', offset);


		}

		$(details).removeClass("invisible-button");

	})


	/************************* ADMIN PANEL *************************/

	window.REMODAL_GLOBALS = {
	  NAMESPACE: 'modal',
	  DEFAULTS: {
	    hashTracking: false
	  }
	};

	//init modal
	var deleteModal = $('[data-remodal-id=modal]').remodal();
	var deleteSurvey;

	//click delete! get modal.
	$('.delete-survey').click(function() {

		//console.log($(this).parent().attr('id'));	//eventually record this to delete from db
		deleteSurvey = $(this).parent();
		deleteModal.open();

	});

	//confirm delete, peace out, survey.
	$('.remodal-confirm').click(function() {

		console.log('click confirm', deleteSurvey);
		$(deleteSurvey).detach();

	})

	/************************* USER MANAGEMENT *************************/
	
	$('.add-user').click(function() {
		
		console.log('clicked');
		$('#add-user-form').removeClass('hidden');
		
	})
	
	$('#generate-password').click(function() {
		
		alert("Clicking this should generate a password randomly.");
		
	})
	
	$('#submit-new-user').click(function() {
		
		alert("Clicking this should write new user to database, which should also trigger a refresh of the user-list above.");
		
	})
	
	$('.user .delete').click(function() {
		
		//probably should warn a user that this is permanent.
		$(this).parent().detach();
		
	})

	/************************* SURVEY BUILDER *************************/

	var globalQuestion = $('.survey-question').clone(true);
	var globalRadio = $('.answer-types .radio-buttons').clone(true);
	var globalCheckbox = $('.answer-types .checkboxes').clone(true);

	var questionInt = 0;	//how many questions do we have? begin at 0.
	var displayQuestionInt = 0; 	//tracks # of questions displayed with respect to those added and deleted.

	//init interface: add click actions; store question HTML as a variable
	//delete a question from the survey builder
	$('.delete').click(function(e) {

		id = $(this).attr('id');
			destroyQuestion(id);
			console.log('delete id: ', id);
	})

	//add a new question to the survey builder
	$('#add-question').click(function(e) {

		e.preventDefault();
		buildQuestion();

	})

	//oh god so messy, but need to be sure first Q has listeners
	$('.choose-answer-type').on('change', function() {

			var answerType = this.value;

			if(answerType == 'checkboxes'){

				//look to be sure we haven't already selected checkboxes/radio buttons
				var atParent = $(this).parent();

				//console.log(atParent.find('.radio-buttons')[0])
				//console.log(atParent.find('.checkboxes')[0])

				//if we have rbuttons, remove them.
				if(atParent.find('.radio-buttons')[0] != undefined) {

					//console.log('we have radio buttons already')
					atParent.find('.radio-buttons').detach();
				}

				//if we have don't have checkboxes, add them.
				if(atParent.find('.checkboxes')[0] == undefined) {

					console.log('checkboxes added');

					var cloneBox = globalCheckbox.clone(true);
						cloneBox.appendTo($('.answerType'));

						console.log('clonebox: ', $(cloneBox).find('#add-checkbox'));

					$(cloneBox).find('#add-checkbox').click(function() {

						var parent = $(this).parent().parent();
						//var clone = parent.find('.checkbox-object').first().clone(true);
						console.log('cloning: ', globalCheckbox.find('.checkbox-object'));

						var clone = globalCheckbox.find('.checkbox-object').clone(true);

						clone.find('.delete-option').click(function() {

							$(this).parent().parent().detach();
						})

						$(clone).insertBefore(parent.find('.add-checkbox'));
					})

					$(cloneBox).find('.delete-option').click(function() {

						console.log('clicking delete', $(this).parent().parent());
						$(this).parent().parent().detach();
					})

				}


			} else if(answerType == 'radio') {

				//look to be sure we haven't already selected checkboxes/radio buttons
				var atParent = $(this).parent();

				//if we have checkboxes, remove them.
				if(atParent.find('.checkboxes')[0] != undefined) {

					//console.log('we have checkboxes already')
					atParent.find('.checkboxes').detach();
				}

				//if we have don't have radio buttons, add them.
				if(atParent.find('.radio-buttons')[0] == undefined) {

					//console.log('radio buttons added');
					var cloneRadio = globalRadio.clone(true);
						cloneRadio.appendTo($('.answerType'));

						$(cloneRadio).find('#add-radio').click(function() {

						var parent = $(this).parent().parent();

						console.log('cloning: ', globalRadio.find('.radio-object'));
						var clone = globalRadio.find('.radio-object').clone(true);
						//var clone = parent.find('.radio-object').first().clone(true);

						clone.find('.delete-option').click(function() {

							$(this).parent().parent().detach();
						})
						$(clone).insertBefore(parent.find('#add-radio'));

					})

					$(cloneRadio).find('.delete-option').click(function() {

						console.log('clicking delete');
						$(this).parent().parent().detach();
					})

				}
			}

		});

	$('#survey-questions').sortable({
			axis: "y",
			revert: true,
			cursor: 'pointer',
			items: "> li",
			tolerance: "intersect",
			placeholder: "sortable-placeholder",
			distance: 50,
			stop: function(event, item) {

				console.log("dragging stopped", item.item.attr('id'));
				updateQuestionNumbering();
			}
		});

	//console.log("GLOBALS:", globalRadio, globalCheckbox);

	function buildQuestion() {

		//increment the number of questions we have
		questionInt++;
		displayQuestionInt ++;

		console.log("GLOBAL: ", globalQuestion);

		//create a new question, give it an ID, append to the right div
		var thisQ = globalQuestion.clone().attr('id', questionInt.toString()).insertBefore('#add-question-wrapper');
		console.log('thisq: ', thisQ);

		//modify question text
		$(thisQ).find('.identifier').text(displayQuestionInt + 1);

		//replace delete button's ID with the same unique identifier as its parent Q
		$(thisQ).find('.delete').attr('id', questionInt.toString());

		//delete a question from the survey builder
		//put this here so that you're only adding *one* listener
		$(thisQ).find('.delete').click(function(e) {

			id = $(this).attr('id');
			destroyQuestion(id);
			console.log('delete id: ', id);

		})

		$(thisQ).find('.choose-answer-type').on('change', function() {

			var answerType = this.value;

			if(answerType == 'checkboxes'){

				console.log('checkboxes added');

				var cloneBox = globalCheckbox.clone(true);

				cloneBox.appendTo($(thisQ).find('.answerType'));

				$(cloneBox).find('.add-checkbox').click(function() {
					console.log('cb button clicked', this);
					var parent = $(this).parent();
					//var clone = parent.find('.checkbox-object').first().clone(true);
					var clone = globalCheckbox.find('.checkbox-object').clone(true);

					clone.find('.delete-option').click(function() {

						$(this).parent().parent().detach();
					})

					$(clone).insertBefore(parent.find('.add-checkbox'));

				})

				$(cloneBox).find('.delete-option').click(function() {

					console.log('clicking delete', $(this).parent());
					$(this).parent().parent().detach();
				})


			} else if(answerType == 'radio') {

				console.log('radio buttons added');
				var cloneRadio = globalRadio.clone(true);
				cloneRadio.appendTo($(thisQ).find('.answerType'));

				$(cloneRadio).find('#add-radio').click(function() {

					console.log('button clicked', this);
					var parent = $(this).parent();
					//var clone = parent.find('.radio-object').first().clone(true);
					var clone = globalRadio.find('.radio-object').clone(true);

					clone.find('.delete-option').click(function() {

						$(this).parent().parent().detach();
					})
					$(clone).insertBefore(parent.find('#add-radio'));
				})

				$(cloneRadio).find('.delete-option').click(function() {

					console.log('clicking delete');
					$(this).parent().parent().detach();
				})
			}

		});


	}

	function destroyQuestion(id) {

		console.log('destroy question: ', id, '.survey-question#' + id)
		displayQuestionInt--;
		$('.survey-question#' + id).detach();

		updateQuestionNumbering();
	}

	function updateQuestionNumbering() {

		console.log('we currently have ', displayQuestionInt, 'questions.');
		var i = 0;
		$('.survey-question').each(function() {

			console.log('finding question: ', this);
			$(this).attr('id', i);
			$(this).find('.delete').attr('id', i)
			$(this).find('.identifier').text(i + 1);

			if(i < displayQuestionInt) {

				i++;
			}
		})
	}
	//checkboxes & radio buttons +1s
	$('#add-radio').click(function() {
		console.log('button clicked', this);
		var parent = $(this).parent();
		var clone = parent.find('.radio-object').first().clone(true);
		$(clone).insertBefore(parent.find('#add-radio'));
	})

	$('#add-checkbox').click(function() {

		console.log('cb button clicked', this);
		var parent = $(this).parent().parent();
		var clone = parent.find('.checkbox-object').first().clone(true);
		$(clone).insertBefore(parent.find('#add-checkbox'));/**/
	})

	$('.delete-option').click(function() {

		$(this).parent().detach();
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

	console.log(surveyData);

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
				console.log(data[i].issue_type, i);

			}

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
			console.log($(this).find('.hidden').text(), 'is value')
			return $(this).find('.invisible').text();
		},
		path: 'static/images',
		half: true,
		readOnly:true,
		number:7
	});

	}

	/***************************** save surveys *****************************/

	$('#save-draft').click(function() {

		console.log('you saved a draft -- create an alert');

		var alert = "<div class='twelve columns'<p class='success'>Your survey has been saved as a draft. It has <span class='bold'>not</span> been published.</p></div>"

		$('#save-draft').parent().append(alert);
		$('#save-draft').unbind('click');
		$('#save-draft').addClass('inactive');

	})

	$('#save-publish').click(function() {

		console.log("you've published a survey");
		window.location.href='/saved-survey/';

	})

}) //close ready
