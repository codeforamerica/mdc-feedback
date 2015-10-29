  $(document).ready(function() {

  //console.log("manage users");
  /************************* USER MANAGEMENT *************************/
  
  $('#add-user').click(function() {
    
    //console.log('clicked');
    $('#add-user-form').removeClass('hidden');
    
  })

  $('#submit-new-user').click(function() {
    
    alert("Clicking this should write new user to database, which should also trigger a refresh of the user-list above.");
    
  })
  
  $('.user .delete').click(function() {
    
    //probably should warn a user that this is permanent.
    alert("clicking this should remove this user from the database.");
    $(this).parent().detach();
    
  })
  
  $('.user .edit').click(function() {
    
    //console.log($(this).parent());
    var p = $(this).parent();
    var form = '#edit-user-form';
    
    //prefill fields
    $(form).find('#name').val(p.find('.user-name').text());
    $(form).find('#email').val(p.find('.user-mail').text());
    
    var permission = $(p).find('.user-permissions').text().toLowerCase().split(' ')[1];
    //console.log(permission);
    
    if(permission === 'superuser') {
      
      //console.log('if', permission);  
      $(form).find('#superuser').prop('checked', true);
      $(form).find('#user').prop('checked', false);
      
    } else {
      
      //console.log('else', permission)
      $(form).find("#user").prop('checked', true);
      $(form).find('#superuser').prop('checked', false);
    }
    
    $(form).removeClass('hidden');
    
    
  })
  
  $('#save-user-changes').click(function() {
    
    alert("save user changes to the database");
    $("#edit-user-form").addClass("hidden");
  })
  
}) //close ready
