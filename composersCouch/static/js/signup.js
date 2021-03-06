function profileType() {
    /* controls what form fields are visible based on profile type */
    var inputValue = $("#id_profile_type option:selected").val();
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
    /* Alows for a button group to be used as a radio input */
    var signup = $("#sign-up-form");
    if (signup.length > 0) {
      $(".profile-type").show();
      $("#div_id_profile_type").hide();
      $("#"+$("#id_profile_type option:selected").val()).addClass('active');
      profileType();
      $(".btn-profile-type").click(function() {
          $(this).addClass('active');
          $('#id_profile_type').val([$(this).attr('id')]);
          $('.btn-profile-type').removeClass('active');
          profileType();
      });
    }
});
