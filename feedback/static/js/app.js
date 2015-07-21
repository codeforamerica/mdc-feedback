$(document).ready(function() {
	
	console.log('hello world');
	
	/************************* ADMIN PANELS *************************/
	
	var questionInt = 0;	//how many questions do we have? begin at 0.
	
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
					
					//console.log('checkboxes added');	
					var cloneBox = globalCheckbox.clone(true);
						cloneBox.appendTo($('.answerType'));
						
					$(cloneBox).find('.add-checkbox').click(function() {
						
						var parent = $(this).parent();
						//var clone = parent.find('.checkbox-object').first().clone(true);
						//console.log('cloning: ', globalCheckbox.find('.checkbox-object'));
						var clone = globalCheckbox.find('.checkbox-object').clone(true);
						clone.find('.delete-option').click(function() {
						
							$(this).parent().detach();
						})
						$(clone).insertBefore(parent.find('.add-checkbox'));/**/
					})
					
					$(cloneBox).find('.delete-option').click(function() {
		
						console.log('clicking delete');
						$(this).parent().detach();
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
						
						var parent = $(this).parent();
						
						console.log('cloning: ', globalRadio.find('.radio-object'));
						var clone = globalRadio.find('.radio-object').clone(true);
						//var clone = parent.find('.radio-object').first().clone(true);
						
						clone.find('.delete-option').click(function() {
						
							$(this).parent().detach();
						})
						$(clone).insertBefore(parent.find('#add-radio'));
						
					})
					
					$(cloneRadio).find('.delete-option').click(function() {
		
						console.log('clicking delete');
						$(this).parent().detach();
					})
					
				}
			}
	
		});
	
	var globalQuestion = $('.survey-question').clone(true);
	var globalRadio = $('.answer-types .radio-buttons').clone(true);
	var globalCheckbox = $('.answer-types .checkboxes').clone(true);
	
	//console.log("GLOBALS:", globalRadio, globalCheckbox);
	
	function buildQuestion() {
		
		//increment the number of questions we have
		questionInt++;	
		
		console.log("GLOBAL: ", globalQuestion);
		
		//create a new question, give it an ID, append to the right div
		var thisQ = globalQuestion.clone().attr('id', questionInt.toString()).appendTo('#survey-questions');
		console.log('thisq: ', thisQ);
		
		//modify question text
		$(thisQ).find('.identifier').text(questionInt + 1);
		
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
						
						$(this).parent().detach();
					})
					$(clone).insertBefore(parent.find('.add-checkbox'));/**/
				})
				
				$(cloneBox).find('.delete-option').click(function() {
		
					console.log('clicking delete');
					$(this).parent().detach();
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
						
						$(this).parent().detach();
					})
					$(clone).insertBefore(parent.find('#add-radio'));
				})
				
				$(cloneRadio).find('.delete-option').click(function() {
		
					console.log('clicking delete');
					$(this).parent().detach();
				})
			}
			
			
		
	
		});

	}
		
	function destroyQuestion(id) {
		
		console.log('destroy question: ', id, '.survey-question#' + id)
		$('.survey-question#' + id).detach();
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
		var parent = $(this).parent();
		var clone = parent.find('.checkbox-object').first().clone(true);
		$(clone).insertBefore(parent.find('#add-checkbox'));/**/
	})
	
	$('.delete-option').click(function() {
		
		$(this).parent().detach();
	})
	
}) //close ready