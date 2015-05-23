import uuid

from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse


def progress_bar():
    """
    progress_bar simple tag

    return html5 tag to display the progress bar
    and url of ajax function needed to get upload progress
    in js/progress_bar.js file.
    """
    progress_bar_tag = '<progress id="progressBar" ' \
        'data-progress_bar_uuid="%s" style="width:100%%" value="0" max="100" ' \
        'hidden></progress>' % (uuid.uuid4())
    upload_progress_url = '<script>upload_progress_url = "%s"</script>' \
        % (reverse('upload_progress'))
    return mark_safe(progress_bar_tag + upload_progress_url)

ProgressBarGlobals = {
    'progress_bar': progress_bar,
}
