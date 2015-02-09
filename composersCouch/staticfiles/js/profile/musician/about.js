$(document).ready(function() {
    artistAboutModals();
    $(".modal").on('hidden.bs.modal', function () {
        window.location.reload(false);
    });
});

$(document).ajaxStop(function() {
    artistAboutModals();
});

function artistAboutModals() {
    modalConnect('.editMusicianBiography','#biographyMusicianForm');
    modalConnect('.editMusicianContact','#contactMusicianForm');
    modalConnect('.editMusicianMembers','#membersMusicianForm');
}
