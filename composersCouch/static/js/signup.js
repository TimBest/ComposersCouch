function profileType() {
  var inputValue = $("input[type=radio]:checked").val();
  if (inputValue=="f") {
    $("#div_id_first_name").show();
    $("#div_id_last_name").show();
    $("#div_id_band_name").hide();
    $("#div_id_venue_name").hide();
  }
  else if (inputValue=="m") {
    $("#div_id_first_name").hide();
    $("#div_id_last_name").hide();
    $("#div_id_band_name").show();
    $("#div_id_venue_name").hide();
  }
  else if (inputValue=="v") {
    $("#div_id_first_name").hide();
    $("#div_id_last_name").hide();
    $("#div_id_band_name").hide();
    $("#div_id_venue_name").show();
  }
}
$(document).ready(function() {
  $(".profile-type").show();
  $("#div_id_profile_type").hide();
  var inputValue = "#" + $("input[type=radio]:checked").val();
  $(inputValue).addClass('active');
  $("#f").click(function() {
    $('button').removeClass('active');
    $(this).addClass('active');
    $('input[type=radio]').val(['f']);
    profileType();
  });
  $("#m").click(function() {
    $('button').removeClass('active');
    $(this).addClass('active');
    $('input[type=radio]').val(['m']);
    profileType();
  });
  $("#v").click(function() {
    $('button').removeClass('active');
    $(this).addClass('active');
    $('input[type=radio]').val(['v']);
    profileType();
  });
  $("input[type=radio]").change(profileType()).change();

});
