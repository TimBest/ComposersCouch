function zipcode_fix() {
    /* Fixes the case when user submits the form before autocomplete can select a valid option */
    code = $("#id_zip_code-autocomplete").val();
    if ($('#id_zip_code option:selected').length==0) {
        $("#id_zip_code").append("<option value='"+code+"' selected='selected'>"+code+"</option>");
    }
}
