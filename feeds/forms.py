from django import forms


from models import Follow, Post
from post_feedly import feedly
from contact.forms import ZipcodeForm


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        widgets = {
          'message' : forms.Textarea(attrs={'rows': 3,}),
        }
        fields = ['message',]

class RemovePostForm(forms.Form):

    class Meta:
        model = Post

    def save(self, user, post):
        if post.user == user:
            # remove post from all feeds
            feedly.remove_post(post)
            return None
        elif post.target == user:
            # remove post from just the tragets feed
            activity = post.create_activity()
            user_feed = feedly.get_user_feed(user.id)
            user_feed.remove(activity)
            return None
        return post

class AvailabilityForm(forms.Form):
    date = forms.DateField(label="Availability", required=False)
    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        self.fields['date'].label = ''

class ZipcodeForm(ZipcodeForm):
    def __init__(self, *args, **kwargs):
        super(ZipcodeForm, self).__init__(*args, **kwargs)
        self.fields['zip_code'].label = ''

class FollowForm(forms.Form):

    class Meta:
        model = Follow
        exclude = ['created_at']

    def save(self, user, target):
        follow, created = Follow.objects.get_or_create(user=user, target_id=target.id)
        if created:
            feedly.follow_user(follow.user_id, follow.target_id)
        else:
            # user is already following target
            feedly.unfollow_user(follow.user_id, follow.target_id)
            follow.delete()
        return follow
