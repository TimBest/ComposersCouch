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
    success:function(data, textStatus, jqXHR){
      $('.reply-form').removeClass("ajax-form-disabled")
      $('.message-list').append(data)
      $(".reply-form")[0].reset();
      updateScroll();
     },
     error: function(jqXHR, textStatus, errorThrown)
     {
       //if fails
     }
   });
   e.preventDefault(); //STOP default action
   //e.unbind('click'); //unbind. to stop multiple form submit.
 });

$(document).ready(function() {
  // allows for text to be entered into auto complete zipcode forms
  $("form").on('submit', function() {
    zipcode_fix();
  });
  // datetimepickers
  $(function () {
      $('#id_date').datetimepicker({pickTime: false});
      $('#id_start_0').datetimepicker({pickTime: false});
      $('#id_start_1').datetimepicker({pickDate: false});
      $('#id_end_0').datetimepicker({pickTime: false});
      $('#id_end_1').datetimepicker({pickDate: false});
      $('#id_accept_by').datetimepicker({pickTime: false});

  });
  // add shows poster js
  function show_image_form() {
    $('#add-poster').hide();
    $('#poster-form').show();
  }
  $(document).ready(function() {
    $('#poster-form').hide();
    $('#poster-form').before(function() {
      return $("<p id='add-poster'><button type='button' class='btn btn-link'><span class='text-muted fa fa-picture-o fa-3x'></span> Attach Photo</button></p>").click(show_image_form);
    })
  });
  // show latest message first
  updateScroll();
});

//Request Participants
function request_participant_form(email_div, user_div) {
  $(email_div).append(function() {
      return $("<a href='#' class='pull-right' id='show-user'>Select by user</a>").click(function(){
          $(email_div).parent().parent().hide();
          $(user_div).show();
      });
  });
  $(user_div).append(function() {
      return $("<a href='#' class='pull-right' id='show-email'>Select by email</a>").click(function(){
          $(user_div).hide();
          $(email_div).parent().parent().show();
        });
  });
  $(email_div).parent().parent().hide();
  $(user_div).show();
}
$(document).ready(function() {
  var messageList = $("#privateRequestForm");
  if (messageList.length > 0){
    request_participant_form("#div_id_email", "#div_id_user");
    request_participant_form("#div_id_form-0-email", "#div_id_form-0-user");
    request_participant_form("#div_id_form-1-email", "#div_id_form-1-user");
    request_participant_form("#div_id_form-2-email", "#div_id_form-2-user");
  }
});

//Show Participants
function show_participant(id, choice_class) {
  $("#div_"+id).hide();
  // get initial data
  $("#div_"+id+" ."+choice_class+" .remove").replaceWith(
    "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"
  );
  $("#div_"+id+"_text .controls").prepend(
    $("#div_"+id+" #"+id+"-deck").html()
  );

  $("#"+id+"_text").yourlabsAutocomplete({
  }).input.bind('selectChoice', function(e, choice, autocomplete) {
    var value = $("#div_"+id+"_text .hilight").attr("data-value");
    // if no selection then add on else remove old selection then add new one
    if ($("#"+id+" option:selected").length==0) {
      $("#"+id+"").append("<option value='"+value+"' selected='selected'>"+value+"</option>");
    } else {
      $("#"+id+" option").replaceWith("<option value='"+value+"' selected='selected'>"+value+"</option>");
      $("#"+id+" option[data-value="+value+"]").remove();
      $("#div_"+id+"_text ."+choice_class).remove();
    }
    // display to user whom they selected
    $("#div_"+id+"_text .controls").prepend(
      "<div class='"+choice_class+"' data-value="+value+">"+
        "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"
        +$(choice).html()+
      "</div>"
    );
  });
  // remove selection display and value
  $("#div_"+id+"_text").on("click", ".remove", function() {
    $("#"+id+" option").remove();
    $(this).parent().remove();
    $("#"+id+"_text").val('');
  });
}

function show_participants(id, choice_class) {
  $("#div_"+id).hide();
  // get initial data
  $("#div_"+id+" ."+choice_class+" .remove").replaceWith(
    "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"
  );
  $("#div_"+id+"_text .controls").prepend(
    $("#div_"+id+" #"+id+"-deck").html()
  );

  $("#"+id+"_text").yourlabsAutocomplete({
  }).input.bind('selectChoice', function(e, choice, autocomplete) {
    var value = $("#div_"+id+"_text .hilight").attr("data-value");
    // if no selection then add on
    $("#"+id).append("<option value='"+value+"' selected='selected'>"+value+"</option>");

    // display to user whom they selected
    $("#div_"+id+"_text .controls").prepend(
      "<div class='"+choice_class+"' data-value="+value+">"+
        "<button class='btn btn-link remove' type='button'><span class='fa fa-times-circle text-muted'></span></button>"
        +$(choice).html()+
      "</div>"
    );
  });

  /* remove selection display and value */
  $("#div_"+id+"_text").on("click", ".remove", function() {
    value = $(this).parent().attr("data-value");
    $("#"+id+" option[value="+value+"]").remove();
    name = $(this).parent().find(".artist-name").text();
    choices = $("#"+id+"_text").val();
    choices = choices.replace(name, "");
    $("#"+id+"_text").val(choices);
    $(this).parent().remove()
  });
}
$(document).ready(function() {
  var eventForm = $("#eventForm");
  if (eventForm.length > 0){
    show_participant("id_headliner", "artist-autocomplete");
    show_participant("id_venue", "user-autocomplete");
    show_participants("id_openers", "artist-autocomplete");
  }
});
