$(document).ready(function () {

  "use strict";
  
  //all the vars, to satisfy the linter.

  var 
      green = "rgba(76, 216, 132, 1)",
      t_green = "rgba(76, 216, 132, 0.2)",
      yellow = "rgba(245, 201, 61, 1)",
      t_yellow = "rgba(245, 201, 61, 0.2)",
      orange = "rgba(243, 155, 121, 1)",
      t_orange = "rgba(243, 155, 121, 0.2)",
      purple = "rgba(61, 51, 119, 1)",
      t_purple = "rgba(61, 51, 119, 0.2)",
      purple_1 = 'rgba(172, 75, 173, 1)',
      t_purple_1 = 'rgba(172, 75, 173, 0.2)',
      purple_2 = 'rgba(122, 0, 134, 1)',
      t_purple_2 = 'rgba(122, 0, 134, 0.2))',
      purple_3 = 'rgba(75, 0, 94, 1)',
      t_purple_3 = 'rgba(75, 0, 94, 0.2)',
      purple_4 = 'rgba(219, 172, 217, 1)',
      t_purple_4 = 'rgba(219, 172, 217, 0.2)',
      blue = 'rgba(93, 205, 252,1)';


  /*$('.pretty-date').each(function() {
    
    //console.log($(this).text());
    $(this).text(prettyDates($(this).text()))  
    $(this).removeClass('hidden');  //keep text from flashing as it gets formatted
    
  })*/
  
  $('.language').each(function() {
    
    var txt = $(this).text();
    
    if(txt == 'en') {
      
      $(this).text('English');
      
    } else {
      
      $(this).text('Spanish');
    }
    
    $(this).removeClass('hidden');
  })
  
  $('.method').each(function() {
    
    var txt = $(this).text();
    
    if(txt == 'sms') {
      
      $(this).addClass('method-sms');
    
    } else {
      
      $(this).addClass('method-web');
    }
    
    $(this).removeClass('hidden');
  })
  
  $('.follow-up').each(function() {
    
    var txt = $(this).text();
    
    if(txt == 'Yes') {
      
      //console.log($(this).parent());
      $(this).parent().addClass('table-alert');
      $(this).parent().append('<tr>This user has requested that you follow up with them.</tr>');
      
    }
  })
  function prettyDates(date) {

    var year = date.split('-')[0];
    var month = String(date.split('-')[1]);   //strict mode means no octal literals -- no 08 or 09 unless type string. A thing I learned today!
    var day = String(date.split('-')[2].split(' ')[0]);
    
    var time = String(date.split(' ')[1]);
   
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

    date = month + '. ' + day + ', ' + year;
    return date;
  }

  
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

  /***************************** star ratings *****************************/

  /*$('#star-rating').raty({
    score: function() {
      //console.log($(this).find('.hidden').text(), 'is value')
      return $(this).find('.invisible').text();
      },
      path: 'static/images',
      half: true,
      readOnly:true,
      number:7
    });*/
    
    $('table').stickyTableHeaders();
    
    
     
}); //close ready
