$(document).ready(function () {

  "use strict";
 
  /* Permitting & violations */

  var ctx2 = $("#openPermits").get(0).getContext("2d"),
      permitJSON = JSON.parse($("#permits_rawjson")[0].childNodes[0].data),
      violationsJSON = JSON.parse($("#violations_rawjson")[0].childNodes[0].data),
      series2 = [],
      datetime2 = [],
      series3 = [],
      datetime3 = [],
      openPermitData,
      openPermitDataset,
      openPermitChart;

  buildOpenPermitChart();
  
  function buildOpenPermitChart() {

    for(var i = 0; i < permitJSON.length; i++) {

      series2.push(permitJSON[i].total);
      datetime2.push(prettyDates((permitJSON[i].month).split('T')[0]));

    }

    series2.reverse();
    datetime2.reverse();

    openPermitDataset = {
        labels:datetime2,
        datasets: [
          {
              fillColor: globalColors.orange_20,
              strokeColor: globalColors.orange,
              pointColor: globalColors.orange,
              pointStrokeColor: "#fff",
              pointHighlightFill: "#fff",
              pointHighlightStroke: "rgba(220,220,220,1)",
              data: series2
          }
        ]
    },

    openPermitChart = new Chart(ctx2).Line(openPermitDataset);

  }
  
  function prettyDates(date) {

    var year = date.split('-')[0];
    var month = String(date.split('-')[1]);   //strict mode means no octal literals -- no 08 or 09 unless type string. A thing I learned today!

    switch (month) {

      case '01':
        month = 'Jan';
        break;
      case '02':
        month = 'Feb';
        break;
      case '03':
        month = 'Mar';
        break;
      case '04':
        month = 'Apr';
        break;
      case '05':
        month = 'May';
        break;
      case '06':
        month = 'Jun';
        break;
      case '07':
        month = 'Jul';
        break;
      case '08':
        month = 'Aug';
        break;
      case '09':
        month = 'Sep';
        break;
      case '10':
        month = 'Oct';
        break;
      case '11':
        month = 'Nov';
        break;
      case '12':
        month = 'Dec';
        break;

    }

    date = month + ' ' + year;
    return date;
  }

  var permitTypes = JSON.parse($("#permitstype")[0].childNodes[0].data),
      pttx = $("#permitTypeChart").get(0).getContext("2d"),
      cleanPermitData = [],
      cleanPermitLabels = [];

  //set the data up for Charts.js
  for(var i = 0; i < permitTypes.data.length; i+=1) {

    if(permitTypes.data[i].permit_type != 'CCUT') {

      cleanPermitLabels.push(humanNames(permitTypes.data[i].permit_type));
      cleanPermitData.push(permitTypes.data[i].count);
      //console.log(data[i].issue_type, i);

    }

  }

  var vdata2 = {
    labels: cleanPermitLabels,
    datasets: [
      {
        label: "Permits by Type",
        fillColor: globalColors.orange_20,
        strokeColor: globalColors.orange,
        data: cleanPermitData
      }
    ]
  };

  function humanNames(type) {

    //console.log(type);

    switch(type) {

      case 'FIRE':

        return 'Fire';
        break;

      case 'MMEC':

        return 'Municipal: Mechanical';
        break;

      case 'ZIPS':

        return 'Zoning Improvement Permit';
        break;

      case 'MELE':

        return 'Muncipal: Electrical';
        break;

      case 'CCUT':

        return 'CCUT';
        break;

      case 'ELEC':

        return 'Electrical';
        break;

      case 'PLUM':

        return 'Plumbing';
        break;

      case 'MPLU':

        return 'Municipal: Plumbing';
        break;

      case 'MBLD':

        return 'Municipal: Building';
        break;

      case 'LPGX':

        return 'Liquid Petroleum Gas';
        break;

      case 'BLDG':

        return 'Building';
        break;

      case 'MECH':

        return 'Mechanical';
        break;

    }

  }

  $('#permitTypeChart').parent().parent().find('.headline').html(permitTypes.title);
  var barChart2 = new Chart(pttx).HorizontalBar(vdata2),
  
      plumbingChart = $("#p-plumbing").get(0).getContext("2d"),
      buildingChart = $("#p-building").get(0).getContext("2d"),
      fireChart = $("#p-fire").get(0).getContext("2d"),
      elexChart = $("#p-electrical").get(0).getContext("2d"),
      zoningChart = $("#p-zoning").get(0).getContext("2d"),
      pData = parseInt($('#plumbing-data').text()),
      bData = parseInt($('#building-data').text()),
      fData = parseInt($('#fire-data').text()),
      eData = parseInt($('#electrical-data').text()),
      zData = parseInt($('#zoning-data').text()),
      
      plumbingData = [
        {
          value: pData,
          color:globalColors.orange,
          highlight: globalColors.orange_20,
          label: 'Plumbing: same-day'
        },
        {
          value: (100 - pData),
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: 'Plumbing'
        }
      ],
      
      buildingData = [
        {
          value: bData,
          color:globalColors.orange,
          highlight: globalColors.orange_20,
          label: 'Building: same-day'
        },
        {
          value: (100 - bData),
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: 'Building'
        }
      ],
      
      fireData = [
        {
          value: fData,
          color:globalColors.orange,
          highlight: globalColors.orange_20,
          label: 'Fire: same-day'
        },
        {
          value: (100 - fData),
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: 'Fire'
        }
      ],
      
      elexData = [
        {
          value: eData,
          color:globalColors.orange,
          highlight: globalColors.orange_20,
          label: 'Electrical: same-day'
        },
        {
          value: (100 - eData),
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: 'Electrical'
        }
      ],
      
      zoningData = [
        {
          value: zData,
          color:globalColors.orange,
          highlight: globalColors.orange_20,
          label: 'Zoning: same-day'
        },
        {
          value: (100 - zData),
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: 'Zoning'
        }
      ],
      
      pChart = new Chart(plumbingChart).Pie(plumbingData),
      bChart = new Chart(buildingChart).Pie(buildingData),
      fChart = new Chart(fireChart).Pie(fireData),
      eChart = new Chart(elexChart).Pie(elexData),
      zChart = new Chart(zoningChart).Pie(zoningData);

  /***************************** tool tips *****************************/
  //called from dashboard-common.js

  initTabletop();

}); //close ready
