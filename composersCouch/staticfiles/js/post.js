$(document).ready(function() {
    $("#post-form").hide();
    $("#attach-photo-form").hide();
    $("#show-post-form").unbind('click');
    $("#show-post-form").click(function() {
        $("#post-form").show();
        $("#show-post-form").hide();
    });
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
