from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import UpdateView

from accounts.utils import update_profile_weight
from artist.models import ArtistProfile
from annoying.functions import get_object_or_None
from contact.views import ContactView
from contact.forms import NonUserLocationForm
from customProfile.views import ArtistProfileView, ArtistProfileFormMixin
from artist.models import Member
from artist.forms import BiographyForm, MemberForm


class AboutView(ArtistProfileView):
    template_name = 'artist/about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        artist_profile = context['artist_profile']
        context['members'] = artist_profile.members.filter(current_member=True)
        return context

about = AboutView.as_view()

class BiographyView(ArtistProfileFormMixin, UpdateView):
    form_class = BiographyForm
    template_name = 'artist/forms_biography.html'
    model = ArtistProfile
    success_url = 'artist:about'

    def get_object(self, queryset=None):
        return self.user.profile.artist_profile

    def get_success_url(self):
        update_profile_weight(user=self.user)
        return reverse(self.success_url, kwargs={'username': self.user.username})

biography = BiographyView.as_view()

class ContactInfoView(ArtistProfileFormMixin, ContactView):
    success_url = 'artist:about'
    template_name = 'artist/forms_contact.html'

    def get_context_data(self, **kwargs):
        context = super(ContactInfoView, self).get_context_data(**kwargs)
        context['contact_type'] = 'band'
        return context

contact_info = ContactInfoView.as_view()

class MemberView(ArtistProfileFormMixin, UpdateView):
    form_class = MemberForm
    model = Member
    member_id=None
    template_name = 'artist/forms_member.html'
    success_url = 'artist:about'

    def dispatch(self, *args, **kwargs):
        member_id = self.kwargs.get('member_id', None)
        self.member = get_object_or_None(self.model, id=member_id)
        return super(MemberView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MemberView, self).get_context_data(**kwargs)
        members = self.user.profile.artist_profile.members
        context['members'] = members.filter(current_member=True).order_by('name')
        context['past_members'] = members.filter(current_member=False).order_by('name')
        context['member'] = self.member
        return context

    def get_object(self, queryset=None):
        return self.member

    def form_valid(self, form):
        form.save(artist=self.user.profile.artist_profile)
        return redirect(self.success_url, username=self.user.username)

members = MemberView.as_view()

class MusicianContactsView(ArtistProfileFormMixin, ContactView):
    locationForm = NonUserLocationForm
    template_name = 'artist/forms_contact.html'
    success_url = 'artist:about'
    contact_type = None
    CONTACT_TYPES = {
        'booking':'booking_contact',
        'label':'label_contact',
        'management':'management_contact',
        'press':'press_contact',
    }

    def dispatch(self, *args, **kwargs):
        if not self.contact_type:
            self.contact_type = self.kwargs.get('contact_type', None)
        if self.contact_type not in self.CONTACT_TYPES:
            self.contact_type = self.CONTACT_TYPES.keys()[0]
        return super(MusicianContactsView, self).dispatch(*args, **kwargs)

    def get_contact_info(self):
        return getattr(self.user.profile.artist_profile, self.CONTACT_TYPES[self.contact_type])

    def set_contact_info(self, contact_info):
        setattr(self.user.profile.artist_profile, self.CONTACT_TYPES[self.contact_type],contact_info)
        self.user.profile.artist_profile.save()
        return contact_info

    def get_context_data(self, **kwargs):
        context = super(MusicianContactsView, self).get_context_data(**kwargs)
        context['contact_type'] = self.contact_type
        return context

contacts = MusicianContactsView.as_view()
