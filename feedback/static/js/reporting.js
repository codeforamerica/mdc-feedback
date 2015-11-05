$(document).ready(function () {
  
  console.log('hello world');

/******************* HAPPY PDF-ING ********************/
	
	$('#pdf').click(function() {
  	
  	$('#test-pdf').prepend($('#reports-view'));
  	return xepOnline.Formatter.Format('test-pdf', {render:'download'});
		
  })
  
  
		//var appended = 0; 
		
		//$('#test-pdf').prepend("<h4>This is a record of your STEP information.</h4>")
				
   // $('#reports-view').each(function() {
      
      
      
   // })
    
		/*$('.module').each(function() {
			
			if($(this).hasClass('hidden') == false ) {
				
				$('#test-pdf').prepend($(this));
				appended++;
			}
			
		})
		
		if(appended == 0) {
			
			$('#test-pdf').append("It looks like we don't have any information specific to your case. ");
		}*/
		
		
			
	

});