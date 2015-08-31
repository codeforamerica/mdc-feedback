	$(document).ready(function() {

	/************************* USER MANAGEMENT *************************/
	
	$('.add-user').click(function() {
		
		//console.log('clicked');
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
	
}) //close ready
