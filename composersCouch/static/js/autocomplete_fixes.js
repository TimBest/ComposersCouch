function zipcode_fix() {
  /* Fixes edge case when user submits the form before autocomplete can select an option */
  $("form").on('submit', function() {
    code = $("#id_zip_code-autocomplete").val();
    $("#id_zip_code").append("<option value='"+code+"' selected='selected'>"+code+"</option>");
  });
}
