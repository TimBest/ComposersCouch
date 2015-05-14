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
