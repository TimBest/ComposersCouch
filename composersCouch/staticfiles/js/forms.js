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
