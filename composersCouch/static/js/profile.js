//about pages
function artistAboutModals() {
    modalConnect('.editMusicianBiography','#biographyMusicianForm');
    modalConnect('.editMusicianContact','#contactMusicianForm');
    modalConnect('.editMusicianMembers','#membersMusicianForm');
}
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
$(document).ready(function() {
    artistAboutModals();
    venueAboutModals();
    $(".modal").on('hidden.bs.modal', function () {
        window.location.reload(false);
    });
});
$( document ).ajaxStop( function() {
    artistAboutModals();
    venueAboutModals();
});


// Track Player Script
$(document).ready(function() {
  $('.json_playlist').each( function (index, data) {
      var id = $(this).attr('id');
      var playlist = jQuery.parseJSON($(this).text());
      var myPlaylist = new jPlayerPlaylist({
        jPlayer: "#jquery_jplayer_"+id,
        cssSelectorAncestor: "#jp_container_"+id
      },
      playlist,
      {
        playlistOptions: {
          enableRemoveControls: false
        },
        swfPath: "/js",
        supplied: "ogv, m4v, oga, mp3",
        keyEnabled: true,
        displayTime: 0,
        audioFullScreen: false // Allows the audio poster to go full screen via keyboard
      });
      $('#jquery_jplayer_'+id).hide();
  });
});

// News Feed post
$(document).ready(function() {
    $("#attach-photo-form").hide();
    $("#attach-photo").unbind('click');
    $("#attach-photo").click(function() {
        $("#attach-photo-form").toggle();
    });
    if ($(".help-block").length) {
      $("#post-form").show();
      $("#show-post-form").hide();
      $("#attach-photo-form").show();
    }
});
