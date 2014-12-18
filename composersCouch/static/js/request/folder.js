function displayFolderControls() {
  if($(".request-folder-checkbox:checked").length > 0) {
    $(".request-folder-actions").show();
  } else {
    $(".request-folder-actions").hide();
  }
}

$(document).ready(function() {
  displayFolderControls();
    $(".request-folder-checkbox").click(function(e) {
      displayFolderControls();
    });
});
