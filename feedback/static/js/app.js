$(document).ready(function() {
	
	console.log('hello world');
	
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
		var thisQ = globalQuestion.clone().attr('id', questionInt.toString()).appendTo('#survey-questions');
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
	
	console.log("DASH: ", $('#dashboard')[0]);	
	
	if($("#dashboard")[0] != undefined) {
		
		// Get context with jQuery - using jQuery's .get() method.
	var ctx = $("#myChart").get(0).getContext("2d");

	var jsondata = JSON.parse($("#jsondata")[0].childNodes[0].data);
	console.log(jsondata);
	
	var series = jsondata.series[0].data;
	var datetime = jsondata.datetime.data;
	console.log(series, datetime);

	var data = {
	    labels: datetime,
	    datasets: [
	        {
	            label: "My First dataset",
	            fillColor: "rgba(220,220,220,0.2)",
	            strokeColor: "rgba(220,220,220,1)",
	            pointColor: "rgba(220,220,220,1)",
	            pointStrokeColor: "#fff",
	            pointHighlightFill: "#fff",
	            pointHighlightStroke: "rgba(220,220,220,1)",
	            data: series
	        }
	        
	    ]
	};

	var myLineChart = new Chart(ctx).Line(data);
	
	
	/***************************** star ratings *****************************/
	
	$('#star-rating').raty({
		score: function() {
			console.log($(this).find('.huge').text(), 'is value')
			return $(this).find('.huge').text();
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