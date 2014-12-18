from django.shortcuts import redirect

from annoying.functions import get_object_or_None
from composersCouch.views import MultipleFormsView
from customProfile.views import ProfileFormMixin
from contact.forms import LocationForm, ContactForm
from contact.models import Zipcode, ContactInfo


class ContactView(ProfileFormMixin, MultipleFormsView):
    locationForm = LocationForm
    contactForm = ContactForm
    template_name = 'profile/forms/contact.html',
    success_url = 'redirectToProfile'

    def get_contact_info(self):
        return self.user.profile.contact_info

    def set_contact_info(self, contact_info):
        self.user.profile.contact_info = contact_info
        self.user.profile.save()
        return contact_info

    def get_objects(self):
        contact_info = self.get_contact_info()
        location_data = {}
        if contact_info:
            location = contact_info.location
            contact = contact_info.contact
        else:
            location = contact = None
        return {
            'location': location,
            'location_data': location_data,
            'contact': contact,
        }
    def get_forms(self, contact_info=None):
        form_kwargs = self.get_form_kwargs()
        objects = self.get_objects()
        locationForm = self.locationForm(data=form_kwargs.get('data'),
                                         instance=objects['location'],
                                         initial=objects['location_data'])
        contactForm = self.contactForm(instance=objects['contact'],
                                       **form_kwargs)
        return {'locationForm':locationForm, 'contactForm':contactForm}

    def forms_valid(self, forms):
        location = forms['locationForm'].save()
        contact = forms['contactForm'].save()
        contact_info = self.get_contact_info()
        if not contact_info:
            contact_info = ContactInfo.objects.create(location=location,
                                                      contact=contact)
        contact_info.save()
        self.set_contact_info(contact_info)
        return redirect(self.success_url, username=self.kwargs.get('username'))
