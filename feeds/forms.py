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
from genres.models import Genre


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
            Submit('submit', 'submit', css_class='btn btn-primary'),
        )

class GenreForm(ModelForm):
    usersGenres = forms.BooleanField(label="My genres", required=False)
    genre = forms.ModelMultipleChoiceField(label="",
              queryset=Genre.objects.all(), required=False,
              widget=MultipleChoiceWidget('GenreAutocomplete'))
    def __init__(self, *args, **kwargs):
        super(GenreForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'genre',
            Div(
              Div('usersGenres',css_class='col-xs-6 left',),
              Div(
                Submit('submit', 'Filter', css_class='btn btn-default pull-right'),
                css_class='col-xs-6 right',css_id='end-div',
              ),
              css_class='row no-gutter',
            ),
        )

    class Meta:
        model = Genre
        fields = ('genre',)

class ZipcodeForm(ZipcodeForm):
    def __init__(self, *args, **kwargs):
        super(ZipcodeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['zip_code'].label = ''
        self.helper.form_tag = False
        self.helper.layout = Layout(
            'zip_code',
            Submit('submit', 'submit', css_class='btn btn-primary'),
        )

class FollowForm(forms.Form):

    class Meta:
        model = Follow
        exclude = ['created_at']

    def save(self, user, target):
        follows = get_object_or_None(Follow, user=user.id, target=target.id)

        if follows:
            feedly.unfollow_user(follows.user_id, follows.target_id)
            follows.delete()
            return

        follow = Follow.objects.create(user=user, target_id=target.id)
        feedly.follow_user(follow.user_id, follow.target_id)
        return follow
