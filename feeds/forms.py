from django import forms
from django.utils.translation import ugettext as _

from autocomplete_light import MultipleChoiceWidget
from autocomplete_light import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Div, Layout, Submit

from models import Follow, Post
from post_feedly import feedly
from annoying.functions import get_object_or_None
from contact.forms import ZipcodeForm


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field('message', placeholder="Message"),
        )

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
        self.helper = FormHelper()
        self.fields['date'].label = ''
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'date',
            Submit('submit', 'Submit', css_class='btn btn-default'),
        )

class ZipcodeForm(ZipcodeForm):
    def __init__(self, *args, **kwargs):
        super(ZipcodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['zip_code'].label = ''
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'zip_code',
            Submit('submit', 'Submit', css_class='btn btn-default'),
        )

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
