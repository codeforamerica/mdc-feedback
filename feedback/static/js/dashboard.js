$(document).ready(function () {

  "use strict";

  /***************************** CHARTS! *****************************/

  //surveys by role
  var sctx = $("#s-role-chart").get(0).getContext("2d"),
      sctxdata = JSON.parse($("#surveyrole")[0].childNodes[0].data),
      sctxseries = [],
      sctxlabels = [],

      //this only works because it's a known quantity.
      homeowners = {label:'Homeowners', count:0},
      architects = {label:'Architects', count:0},
      contractors = {label:'Contractors', count:0},
      consultants = {label:'Permit Consultants', count:0},
      owners = {label:'Business Owners', count:0},
      sorter = [architects, owners, consultants, contractors, homeowners],
      i,
      respondentsByRole,
      respondentsByRoleChart;

  for(i = 0; i < sctxdata.data.length; i+=1) {

    switch(parseInt(sctxdata.data[i][0], 10)) {

      case 1:
        contractors.count = sctxdata.data[i][1];
        break;
      case 2:
        architects.count = sctxdata.data[i][1];
        break;
      case 3:
        consultants.count = sctxdata.data[i][1];
        break;
      case 4:
        homeowners.count = sctxdata.data[i][1];
        break;
      case 5:
        owners.count = sctxdata.data[i][1];
        break;

    }

  }

  for(i = 0; i < sorter.length; i+=1) {

    sctxseries[i] = sorter[i].count;
    sctxlabels[i] = sorter[i].label;

  }

  respondentsByRole = {
    labels: sctxlabels,
    datasets: [
      {
          label: "Respondents by Role",
          fillColor: globalColors.orange_20,
          strokeColor: globalColors.orange,
          data: sctxseries
      }
    ]
  };

  respondentsByRoleChart = new Chart(sctx).HorizontalBar(respondentsByRole);

  // end surveys by role

  // successful task completion
  var cctx = $("#s-complete-chart").get(0).getContext("2d"),
      cctxdata = JSON.parse($("#surveycomplete")[0].childNodes[0].data),
      total = cctxdata.data.total,
      completeTrue = cctxdata.data.yes,
      completeFalse = total - completeTrue,

    cctxPie = [
    {
      value: completeTrue,
      color:globalColors.orange,
      highlight: globalColors.orange_20,
      label: 'Successfully completed task'
    },
    {
      value: completeFalse,
      color: globalColors.orange_60,
      highlight: globalColors.orange_20,
      label: 'Failed to complete task'
    }
  ],

  cctxPieChart = new Chart(cctx).Pie(cctxPie),
  // end successful task completion

  // surveys by purpose
  sptx = $("#s-purpose-chart").get(0).getContext("2d"),
  sptxdata = JSON.parse($("#surveypurpose")[0].childNodes[0].data),

  //this only works because it's a known quantity.
  violation = {label:'Find out about a violation/lien', count:0},
  inspector = {label:'Meet with an inspector', count:0},
  permit = {label:'Apply for a permit', count:0},
  reviewer = {label:'Meet with a plan reviewer', count:0},
  cu = {label:'Obtain a certificate of use/occupancy', count:0},
  other = {label:'Other', count:0},
  sorter2 = [violation, inspector, permit, reviewer, cu, other],

  sptxseries = [],
  sptxlabels = [],
  surveysByPurpose,
  surveysByPurposeChart;

  var test = 0;

  for(i = 0; i < sptxdata.data.length; i+=1) {

    switch(parseInt(sptxdata.data[i][0], 10)) {

      case 1:
        permit.count += sptxdata.data[i][1];
        break;
      case 2:
        inspector.count += sptxdata.data[i][1];
        break;
      case 3:
        reviewer.count += sptxdata.data[i][1];
        break;
      case 4:
        violation.count += sptxdata.data[i][1];
        break;
      case 5:
        cu.count += sptxdata.data[i][1];
        break;
      case 6:
        other.count += sptxdata.data[i][1];
      default:
        other.count += 1;

    }

  }

  for(i = 0; i < sorter2.length; i+=1) {
    sptxseries[i] = sorter2[i].count;
    sptxlabels[i] = sorter2[i].label;
  }

  surveysByPurpose = {
    labels: sptxlabels,
    datasets: [
      {
        label: "Respondents by Purpose",
        fillColor: globalColors.orange_20,
        strokeColor: globalColors.orange,
        data: sptxseries
      }
    ]
  };

  surveysByPurposeChart = new Chart(sptx).HorizontalBar(surveysByPurpose);
  // end surveys by purpose
  
  // Get context with jQuery - using jQuery's .get() method.
  var ctx = $("#myChart").get(0).getContext("2d"),
      jsondata = JSON.parse($("#jsondata")[0].childNodes[0].data),
      series = jsondata.series[0].data,
      datetime = jsondata.datetime.data,

      data = {
        labels: datetime,
        scaleBeginAtZero: true,
        datasets: [
            {
                fillColor: globalColors.orange_20,
                strokeColor: globalColors.orange,
                pointColor: globalColors.orange,
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: series,
                scaleStartValue: 0
            }
        ]
      },

      myPieChart,
      myLineChart = new Chart(ctx).Line(data),
      surveyData = JSON.parse($("#surveydata")[0].childNodes[0].data),
      pctx = $("#surveyChart").get(0).getContext("2d"),

      pieData = [
        {
          value: surveyData.data.web_en,
          color: globalColors.orange,
          highlight: globalColors.orange_20,
          label: surveyData.labels.web_en
        },
        {
          value: surveyData.data.web_es,
          color: globalColors.orange_80,
          highlight: globalColors.orange_20,
          label: surveyData.labels.web_es
        },
        {
          value: surveyData.data.sms_en,
          color: globalColors.orange_60,
          highlight: globalColors.orange_20,
          label: surveyData.labels.sms_en
        },
        {
          value: surveyData.data.sms_es,
          color: globalColors.orange_40,
          highlight: globalColors.orange_20,
          label: surveyData.labels.sms_es

        }
      ];

      $('#surveyChart').parent().parent().find('.headline').html(surveyData.title);
      myPieChart = new Chart(pctx).Pie(pieData);

  /***************************** star ratings *****************************/

  $('#star-rating').raty({
    score: function() {
      //console.log($(this).find('.hidden').text(), 'is value')
      return $(this).find('.invisible').text();
      },
      path: 'static/images',
      half: true,
      readOnly:true,
      number:7
    });

    $('#s-lang-rate-en').raty({
    score: function() {
      //console.log($(this).find('.hidden').text(), 'is value')
      return $('#rate-en').text();
      },
      path: 'static/images',
      half: true,
      readOnly:true,
      number:7
    });

    $('#s-lang-rate-es').raty({
      score: function() {
        return $('#rate-en').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-permit').raty({
      score: function() {
        return $('#rate-permit').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-inspect').raty({
      score: function() {
        return $('#rate-inspect').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-review').raty({
      score: function() {
        return $('#rate-review').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-liens').raty({
      score: function() {
        return $('#rate-liens').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-purpose-rate-cu').raty({
      score: function() {
        return $('#rate-cu').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-permit').raty({
      score: function() {
        return $('#role-rate-permit').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-cu').raty({
      score: function() {
        return $('#role-rate-cu').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-inspect').raty({
      score: function() {
        return $('#role-rate-inspect').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-review').raty({
      score: function() {
        return $('#role-rate-review').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

    $('#s-role-rate-lien').raty({
      score: function() {
        return $('#role-rate-lien').text();
        },
        path: 'static/images',
        half: true,
        readOnly:true,
        number:7
    });

  /***************************** tool tips *****************************/
  //called from dashboard-common.js

  initTabletop();

}); //close ready
