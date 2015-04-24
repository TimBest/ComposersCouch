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
