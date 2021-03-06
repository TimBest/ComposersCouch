function show_image_picker() {
    $(uploadDiv).hide();
    $(selectDiv).show();
}
function show_image_uploader() {
    $(selectDiv).hide();
    $(uploadDiv).show();
}
$(document).ready(function() {
    if (typeof selectorId != 'undefined') {
        $(selectorId).imagepicker({show_label : true});
        if (images) {
          $(uploadDiv).append(function() {
            return $("<a href='#' id='show-image-picker'>Select from my photos</a>").click(
              function() {
                $(uploadDiv).hide();
                $(selectDiv).show();
              }
            );
          });
        }
        $(selectDiv).append(function() {
          return $("<a href='#' id='show-image-uploader'>Upload photo</a>").click(
            function() {
              $(selectDiv).hide();
              $(uploadDiv).show();
            }
          );
        });
        show_image_uploader();
        if ($(".help-block").length) {
          show_image_uploader();
        }
    }
});
