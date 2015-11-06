$(document).ready(function () {
  
  /******************* HAPPY PDF-ING ********************/
	
	$('#pdf').click(function(e) {
  	
  	e.preventDefault();
  	$('#print-to-pdf').append($("#report-title"));
  	
  	$('.print-this').each(function() {
    	
    	$('#print-to-pdf').append($(this));
    	//console.log($(this).text());
    	
  	})
  	
  	return xepOnline.Formatter.Format('print-to-pdf', {render:'embed', filename:'monthly_report'});
		
  })
  
});