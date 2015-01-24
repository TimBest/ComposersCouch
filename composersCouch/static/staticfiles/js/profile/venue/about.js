$(document).ready(function() {
    venueAboutModals();
    $(".modal").on('hidden.bs.modal', function () {
        window.location.reload(false);
    });
});

$( document ).ajaxStop( function() {
    venueAboutModals();
});

function venueAboutModals() {
    modalConnect('.editPolicies','#policiesForm');
    modalConnect('.editStaff','#staffForm');
    modalConnect('.editSeating','#seatingForm');
    modalConnect('.editBiography','#biographyForm');
    modalConnect('.editContact','#contactForm');
    modalConnect('.editEquipment','#equipmentForm', '.deleteEquipment');
    modalConnect('.editHours','#hoursForm');
    $('#id_form-0-start').datetimepicker({pickDate: false});
    $('#id_form-0-end').datetimepicker({pickDate: false});
    $('#id_form-1-start').datetimepicker({pickDate: false});
    $('#id_form-1-end').datetimepicker({pickDate: false});
    $('#id_form-2-start').datetimepicker({pickDate: false});
    $('#id_form-2-end').datetimepicker({pickDate: false});
    $('#id_form-3-start').datetimepicker({pickDate: false});
    $('#id_form-3-end').datetimepicker({pickDate: false});
    $('#id_form-4-start').datetimepicker({pickDate: false});
    $('#id_form-4-end').datetimepicker({pickDate: false});
    $('#id_form-5-start').datetimepicker({pickDate: false});
    $('#id_form-5-end').datetimepicker({pickDate: false});
    $('#id_form-6-start').datetimepicker({pickDate: false});
    $('#id_form-6-end').datetimepicker({pickDate: false});
}
