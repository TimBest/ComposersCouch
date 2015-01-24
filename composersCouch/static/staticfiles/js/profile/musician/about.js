$(document).ready(function() {
    musicianAboutModals();
    $(".modal").on('hidden.bs.modal', function () {
        window.location.reload(false);
    });
});

$(document).ajaxStop(function() {
    musicianAboutModals();
});

function musicianAboutModals() {
    modalConnect('.editMusicianBiography','#biographyMusicianForm');
    modalConnect('.editMusicianContact','#contactMusicianForm');
    modalConnect('.editMusicianMembers','#membersMusicianForm');
}
