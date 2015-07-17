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
	$('#choose-answer-type').on('change', function() {
		
			var answerType = this.value;
			
			if(answerType == 'checkboxes'){
				
				console.log('checkboxes added');	
				globalCheckbox.clone().appendTo($('#answerType'));
			
			} else if(answerType == 'radio') {
				
				console.log('radio buttons added');
				globalRadio.clone().appendTo($('#answerType'));
			}
			
		});
	
	var globalQuestion = $('.survey-question').clone(true);
	var globalRadio = $('#answer-types #radio-buttons').clone(true);
	var globalCheckbox = $('#answer-types #checkboxes').clone(true);
	
	console.log("GLOBALS:", globalRadio, globalCheckbox);
	
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
		
		$(thisQ).find('#choose-answer-type').on('change', function() {
		
			var answerType = this.value;
			
			if(answerType == 'checkboxes'){
				
				console.log('checkboxes added');	
				globalCheckbox.clone().appendTo($(thisQ).find('#answerType'));
			
			} else if(answerType == 'radio') {
				
				console.log('radio buttons added');
				globalRadio.clone().appendTo($(thisQ).find('#answerType'));
			}
			
		});

	}
		
	function destroyQuestion(id) {
		
		console.log('destroy question: ', id, '.survey-question#' + id)
		$('.survey-question#' + id).detach();
	}
	
		
		
	
}) //close ready