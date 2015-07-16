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
	
	var globalQuestion = $('.survey-question').clone();
	
	function buildQuestion() {
		
		//increment the number of questions we have
		questionInt++;	
		
		console.log("GLOBAL: ", globalQuestion);
		
		//create a new question, give it an ID, append to the right div
		//$('.survey-question#' + questionInt.toString()).clone().attr('id', 'new-q').appendTo('#survey-questions');

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
		
		//assign new value as unique ID to question; replaces 'new-q' from above
		//you're using the unique ID as a way to target the element to clone
		/*$('#new-q').attr('id', questionInt.toString());	*/
	}
		
	function destroyQuestion(id) {
		
		console.log('destroy question: ', id, '.survey-question#' + id)
		$('.survey-question#' + id).detach();
	}
	
}) //close ready