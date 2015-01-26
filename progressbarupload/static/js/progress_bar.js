// Generate 32 char random uuid
function gen_uuid() {
  var uuid = ""
  for (var i=0; i < 32; i++) {
    uuid += Math.floor(Math.random() * 16).toString(16);
  }
  return uuid
}

// Add upload progress for multipart forms.
$(document).ready(function(){
  $('form').submit(function(){
    // Prevent multiple submits
    if ($.data(this, 'submitted')) return false;

    var freq = 10;//1000; // freqency of update in ms
    var uuid = gen_uuid(); // id for this upload so we can fetch progress info.
    var progress_url = upload_progress_url; // ajax view serving progress info

    // Append X-Progress-ID uuid form action
    this.action += (this.action.indexOf('?') == -1 ? '?' : '&') + 'X-Progress-ID=' + uuid;

    var $progress = $('<div class="progress"></div>').
    appendTo('form').append('<div class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="min-width: 2em;"><span class="progress-info">0%</span></div>');

    // progress bar position
    $progress.show();

    // Update progress bar
    function update_progress_info() {
      $progress.show();
      $.getJSON(progress_url, {'X-Progress-ID': uuid}, function(data, status){
        if (data) {
          var progress = parseInt(data.uploaded) / parseInt(data.length);
          var width = $progress.find('.progress-container').width()
          var progress_width = width * progress;
          $progress.find('.progress-bar').width(progress_width);
          $progress.find('.progress-bar').attr("aria-valuenow="+progress_width);
          $progress.find('.progress-info').text('uploading ' + parseInt(progress*100) + '%');
        }
        window.setTimeout(update_progress_info, freq);
      });
    };
    window.setTimeout(update_progress_info, freq);

    $.data(this, 'submitted', true); // mark form as submitted.
  });
});
