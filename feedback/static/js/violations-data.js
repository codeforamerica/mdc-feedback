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

  var vioTypeData = JSON.parse($("#violations_type_json")[0].childNodes[0].data);
  
  if(vioTypeData === '') {

      $('#regulation h3').append("<div class='alert-alert-warning'><p class='alert center small'>Sorry, something's gone wrong with our data for neighborhood compliance! <br>We're working to get it back online.</p></div>");

  } else {

    var labels = [];
    var dataset = [];

    //the 'total' isn't an integer. make it one, or the sort will fail.
    for(i = 0; i < vioTypeData.length;   i+=1) {

      vioTypeData[i].total = parseInt(vioTypeData[i].total, 10);
      //console.log(data[i]);
    }

    //sort on the number of each violation type
    vioTypeData = vioTypeData.sortOn("total");
    vioTypeData.reverse();

    //set the data up for Charts.js
    for(i = 0; i < vioTypeData.length;   i+=1) {

      labels[i] = vioTypeData[i].issue_type;
      dataset[i] = vioTypeData[i].total;
      //console.log(data[i].issue_type, i);

    }

    labels.reverse();
    dataset.reverse();

    //create the chart
    var bctx = $("#viotype").get(0).getContext("2d");

    var bdata = {
        labels: labels,
        datasets: [
            {
              fillColor: t_purple_1,
              strokeColor: purple_1,
              data: dataset
            }
        ]
    };

    var horizontalBarChart = new Chart(bctx).HorizontalBar(bdata);

  }
    
}) //close ready
