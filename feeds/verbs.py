from stream_framework.verbs import register
from stream_framework.verbs.base import Verb

# apparently id 1-4 are reserved
class Post(Verb):
    id = 5
    infinitive = 'post'
    past_tense = 'posted'

register(Post)
