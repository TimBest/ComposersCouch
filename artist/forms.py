from django import forms

from models import Member
from artist.models import ArtistProfile


class BiographyForm(forms.ModelForm):

    class Meta:
        model = ArtistProfile
        widgets = {
          'biography' : forms.Textarea(attrs={'rows': 2, 'cols': 19}),
        }
        fields = ('biography',)

class MemberForm(forms.ModelForm):
    remove_member = forms.BooleanField(required=False)

    def save(self, artist):
        delete = self.cleaned_data.get('remove_member', False)
        member = super(MemberForm, self).save(commit=False)
        member.profile = artist
        member.save()
        if delete:
            member.delete()
            return None
        return member

    class Meta:
        model = Member
        widgets = {'biography':forms.Textarea(attrs={'rows': 2, 'cols': 19}),}
        fields = ('name','biography','current_member')
