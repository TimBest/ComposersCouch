// add shows poster js
function show_image_form() {
    $('#add-poster').hide();
    $('#poster-form').show();
}

$(document).ready(function() {
    // allows for text to be entered into auto complete zipcode forms
    $("form").on('submit', function() {
        zipcode_fix();
    });
    // datetimepickers
    $('#id_date').datetimepicker({pickTime: false});
    $('#id_start_0').datetimepicker({pickTime: false});
    $('#id_start_1').datetimepicker({pickDate: false});
    $('#id_end_0').datetimepicker({pickTime: false});
    $('#id_end_1').datetimepicker({pickDate: false});
    $('#id_accept_by').datetimepicker({pickTime: false});

    $('#poster-form').hide();
    $('#poster-form').before(function() {
        return $("<p id='add-poster'><button type='button' class='btn btn-link'><span class='text-muted fa fa-picture-o fa-3x'></span> Attach Photo</button></p>").click(show_image_form);
    })

});
