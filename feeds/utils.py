from feeds.models import Post


def enrich_activities(activities):
    '''
    Load the models attached to these activities
    (Normally this would hit a caching layer like memcached or redis)
    '''
    post_ids = [a.object_id for a in activities]
    post_dict = Post.objects.in_bulk(post_ids)
    for a in activities:
        a.post = post_dict.get(a.object_id)

    return activities
