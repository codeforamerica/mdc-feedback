$(document).ready(function() {
	
	$('.alert .close').click(function(e) {
  	
  	e.preventDefault();
  	$(this).parent().slideUp();
  	
	})
}); //close ready
