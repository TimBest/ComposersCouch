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
}
