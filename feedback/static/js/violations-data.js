$(document).ready(function() {
	
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

	/* VIOLATIONS */

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
			for(var i = 0; i < data.length; i++) {

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
	}) //close ready
