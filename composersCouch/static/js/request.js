// Displays meaage control (read, unread, delete) when/if  checkbox if selected
function displayMessageControls() {
    if($(".request-folder-checkbox:checked").length > 0) {
        $(".request-folder-actions").show();
    } else {
        $(".request-folder-actions").hide();
    }
}

// reply form for threads
function updateScroll(){
    var messageList = $(".messages .message-list");
    if (messageList.length > 0){
        messageList.scrollTop($('.message-list')[0].scrollHeight);
    }
}
$(".messages .reply-form").submit(function(e) {
    var postData = $(this).serializeArray();
    var formURL = $(this).attr("action");
    $.ajax({
        url : formURL,
        type: "POST",
        data : postData,
        success:function(data, textStatus, jqXHR) {
            $('.reply-form').removeClass("ajax-form-disabled")
            $('.message-list').append(data)
            $(".reply-form")[0].reset();
            updateScroll();
         },
         error: function(jqXHR, textStatus, errorThrown) {
            //if fails
         }
    });
    e.preventDefault(); //STOP default action
});

//Request Participants
function request_participant_form(email_div, user_div) {
  $(email_div).append(function() {
      return $("<div class='text-right'><a href='#' id='show-user'>Select by user</a><div>").click(function(){
          $(email_div).parent().parent().hide();
          $(user_div).show();
      });
  });
  $(user_div).append(function() {
      return $("<div class='text-right'><a href='#' id='show-email'>Select by email</a><div>").click(function(){
          $(user_div).hide();
          $(email_div).parent().parent().show();
        });
  });
  $(email_div).parent().parent().hide();
  $(user_div).show();
}

$(document).ready(function() {
    // display message controls if a checkbox is selected
    displayMessageControls();
    $(".request-folder-checkbox").click(function(e) {
        displayMessageControls();
    });
    // show latest message first
    updateScroll();
    // show (Name & email) or select user
    var messageList = $("#privateRequestForm");
    if (messageList.length > 0){
        request_participant_form("#div_id_email", "#div_id_participant");
        request_participant_form("#div_id_form-0-email", "#div_id_form-0-participant");
        request_participant_form("#div_id_form-1-email", "#div_id_form-1-participant");
        request_participant_form("#div_id_form-2-email", "#div_id_form-2-participant");
    }
});
