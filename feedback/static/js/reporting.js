$(document).ready(function () {
  
  /******************* HAPPY PDF-ING ********************/
	
	$('#pdf').click(function() {
  	
  	return xepOnline.Formatter.Format('reports-view', {render:'none', filename:'monthly_report'});
		
  })
  
});