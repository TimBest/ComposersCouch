from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import UpdateView

from artist.models import ArtistProfile
from annoying.functions import get_object_or_None
from contact.views import ContactView
from contact.forms import NonUserLocationForm
from customProfile.views import ArtistProfileView, ProfileFormMixin
from artist.models import Member
from artist.forms import BiographyForm, MemberForm


class AboutView(ArtistProfileView):
    template_name = 'profile/artist/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        artist_profile = context['artist_profile']
        context['members'] = artist_profile.members.filter(current_member=True)
        return context

about = AboutView.as_view()

class BiographyView(ProfileFormMixin, UpdateView):
    form_class = BiographyForm
    template_name = 'profile/artist/forms/biography.html'
    model = ArtistProfile
    success_url = 'artist:about'

    def get_object(self, queryset=None):
        return self.user.profile.artist_profile

    def get_success_url(self):
        return reverse(self.success_url, kwargs={'username': self.user.username})

biography = BiographyView.as_view()

class ContactInfoView(ContactView):
    success_url = 'artist:about'
    template_name = 'profile/artist/forms/contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactInfoView, self).get_context_data(**kwargs)
        context['contactType'] = 'band'
        return context

contact_info = ContactInfoView.as_view()

class MemberView(ProfileFormMixin, UpdateView):
    form_class = MemberForm
    model = Member
    memberID=None
    template_name = 'profile/artist/forms/member.html'
    success_url = 'artist:about'

    def get_context_data(self, **kwargs):
        context = super(MemberView, self).get_context_data(**kwargs)
        band = self.user.profile.artist_profile
        context['members'] = band.members.filter(current_member=True).order_by('name')
        context['past_members'] = band.members.filter(current_member=False).order_by('name')
        context['memberID'] = self.kwargs.get('memberID', None)
        return context

    def get_object(self, queryset=None):
        self.memberID = self.kwargs.get('memberID', None)
        member = get_object_or_None(self.model, id=self.memberID)
        return member

    def form_valid(self, form):
        member = form.save()
        if member:
            member.artist_profile = self.user.profile.artist_profile
            member.save()
        return redirect(self.success_url, username=self.user.username)

members = MemberView.as_view()

class MusicianContactsView(ContactView):
    locationForm = NonUserLocationForm
    template_name = 'profile/artist/forms/contact.html'
    success_url = 'artist:about'
    contactType = None
    CONTACT_TYPES = {
        'booking':'booking_contact',
        'label':'label_contact',
        'management':'management_contact',
        'press':'press_contact',
    }

    def dispatch(self, *args, **kwargs):
        if not self.contactType:
            self.contactType = self.kwargs.get('contactType', None)
        if self.contactType not in self.CONTACT_TYPES:
            self.contactType = self.CONTACT_TYPES.keys()[0]
        return super(ContactView, self).dispatch(*args, **kwargs)

    def get_contact_info(self):
        return getattr(self.user.profile.artist_profile, self.CONTACT_TYPES[self.contactType])

    def set_contact_info(self, contact_info):
        setattr(self.user.profile.artist_profile, self.CONTACT_TYPES[self.contactType],contact_info)
        self.user.profile.artist_profile.save()
        return contact_info

    def get_context_data(self, **kwargs):
        context = super(MusicianContactsView, self).get_context_data(**kwargs)
        context['contactType'] = self.contactType
        return context

contacts = MusicianContactsView.as_view()
