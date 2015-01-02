function zipcode_fix() {
  /* Fixes edge case when user submits the form before autocomplete can select an option */
  $("#sign-up-submit").on('click', function() {
    code = $("#id_zip_code-autocomplete").val();
    $("#id_zip_code").append("<option value='"+code+"' selected='selected'>"+code+"</option>");
  });
}
