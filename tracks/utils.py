import json
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


def safe_json(data):
    return mark_safe(json.dumps(data))

def json_playlist(tracks, album=None, viewname=None, username=None):
    playlist = []
    if album:
        for track in tracks:
            data = {}
            data['title'] = track.media.title
            if track.media.audio:
                data['mp3'] = settings.MEDIA_URL + str(track.media.audio)
            data['order'] = track.order
            playlist.append(data)
    else:
      for count,track in enumerate(tracks, start=1):
          data = {}
          data['title'] = track.media.title
          if track.media.audio:
              data['mp3'] = settings.MEDIA_URL + str(track.media.audio)
          data['order'] = count
          try:
              data['edit_url'] = reverse(viewname, args=(username,track.id))
          except:
              pass
          playlist.append(data)
    return safe_json(playlist)
