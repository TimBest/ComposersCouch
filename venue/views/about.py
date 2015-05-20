from datetime import datetime
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory, modelformset_factory
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import FormView, UpdateView

from accounts.utils import update_profile_weight
from annoying.functions import get_object_or_None
from contact.forms import ContactForm
from contact.views import ContactView
from annoying.views import MultipleModelFormsView
from customProfile.views import VenueProfileView, VenueProfileFormMixin
from photos.forms import SeatingChartForm
from photos.models import Image
from photos.views import ImageFormMixin
from venue.models import VenueProfile
from venue import forms, models


class VenueProfileAboutView(VenueProfileView):
    template_name = 'venue/about.html'

    def get_context_data(self, **kwargs):
        context = super(VenueProfileAboutView, self).get_context_data(**kwargs)
        venueProfile = context['venueProfile']
        context['today'] = datetime.now().weekday()
        context['sound'] = venueProfile.equipment.filter(category='Sound')
        context['effects'] = venueProfile.equipment.filter(category='Effects')
        context['accessories'] = venueProfile.equipment.filter(category='Accessories')
        return context

venue_about = VenueProfileAboutView.as_view()

class BiographyView(VenueProfileFormMixin, UpdateView):
    form_class = forms.BiographyForm
    template_name = 'venue/forms_biography.html'
    model = VenueProfile
    success_url = 'venue:about'

    def get_object(self, queryset=None):
        return self.user.profile.venueProfile

    def get_success_url(self):
        update_profile_weight(user=self.user)
        return reverse(self.success_url, kwargs={'username': self.user.username})

biography = BiographyView.as_view()

class ContactInfoView(VenueProfileFormMixin, ContactView):
    success_url = 'venue:about'
    template_name = 'venue/forms_contact.html'

contact_info = ContactInfoView.as_view()

class EquipmentView(VenueProfileFormMixin, FormView):
    template_name = 'venue/forms_equipment.html'
    success_url = 'venue:about'
    model = models.Equipment
    form_class = forms.EquipmentForm
    category = None
    extra = 3
    CATEGORY_TYPES = {
        'sound'       : 'Sound',
        'effects'     : 'Effects',
        'accessories' : 'Accessories',
    }

    def dispatch(self, *args, **kwargs):
        self.category = self.kwargs.get('category')
        if self.category not in self.CATEGORY_TYPES:
            raise Http404
        return super(EquipmentView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EquipmentView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_form(self, form_class=None):
        formset = modelformset_factory(self.model, self.form_class, extra=self.extra, fields =['id','name','quantity','category',])
        form_kwargs = self.get_form_kwargs()
        equipment = models.Equipment.objects.filter(
                        profile=self.user.profile.venueProfile,
                        category=self.CATEGORY_TYPES[self.category])
        return formset(queryset=equipment, **form_kwargs)

    def form_valid(self, form):
      for f in form:
        if f.has_changed():
            equipment = f.save(commit=False)
            if equipment:
                equipment.profile = self.user.profile.venueProfile
                equipment.category = self.CATEGORY_TYPES[self.category]
                equipment.save()
      return redirect(self.success_url, username=self.user.username)

equipment = EquipmentView.as_view()

class HoursView(VenueProfileFormMixin, FormView):
    template_name = 'venue/forms_hours.html'
    model = models.Hours
    form_class = forms.HoursForm
    success_url = 'venue:about'
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday',]

    def get_context_data(self, **kwargs):
        context = super(HoursView, self).get_context_data(**kwargs)
        context['forms'] = zip(self.weekdays, context['form'])
        return context

    def get_form(self, form_class=None):
        formset = modelformset_factory(self.model, self.form_class, extra=7, max_num=7, fields = ('id','start','end',))
        hours = models.Hours.objects.filter(profile=self.user.profile.venueProfile)
        form_kwargs = self.get_form_kwargs()
        return formset(queryset=hours, **form_kwargs)

    def form_valid(self, form):
        for count,f in enumerate(form):
            hours_old = get_object_or_None(self.model, profile=self.user.profile.venueProfile, weekday=count)
            hours = f.save(commit=False)
            if hours_old:
                hours_old.start = hours.start
                hours_old.end = hours.end
                hours_old.save()
            else:
                hours.profile = self.user.profile.venueProfile
                hours.weekday = count
                hours.save()
        return redirect(self.success_url, username=self.user.username)

hours = HoursView.as_view()

class PoliciesView(VenueProfileFormMixin, FormView):
    template_name = 'venue/forms_policies.html'
    model = models.Policies
    form_class = forms.PoliciesForm
    success_url = 'venue:about'
    extra = 1

    def get_form(self, form_class=None):
        formset = modelformset_factory(self.model, self.form_class, extra=self.extra, exclude=('',))
        policies = self.model.objects.filter(profile=self.user.profile.venueProfile)
        form_kwargs = self.get_form_kwargs()
        return formset(queryset=policies, **form_kwargs)

    def form_valid(self, form):
      for f in form:
        if f.has_changed():
            policy = f.save(commit=False)
            if policy:
                policy.profile = self.user.profile.venueProfile
                policy.save()
      return redirect(self.success_url, username=self.user.username)

policies = PoliciesView.as_view()

class SeatingView(VenueProfileFormMixin, ImageFormMixin, MultipleModelFormsView):
    form_classes = {
      'seatingForm' : forms.SeatingForm,
      'seatingChartForm' : SeatingChartForm
    }
    template_name = 'venue/forms_seating.html'
    model = models.Seating
    success_url = 'venue:about'

    def get_objects(self, queryset=None):
        seating = get_object_or_None(self.model, profile=self.user.profile.venueProfile)
        return {
          'seatingForm' : seating,
          'seatingChartForm' : seating.seating_chart if seating else None
        }

    def forms_valid(self, forms):
        seating = forms['seatingForm'].save(commit=False)
        seating.profile = self.user.profile.venueProfile
        if self.request.FILES.get('image'):
            seating.seating_chart, created = Image.objects.get_or_create(
                image=self.request.FILES.get('image'),
                title = "Seating Chart",
                user = self.user
            )
        elif self.request.POST.get('seating_chart'):
            imageId = self.request.POST.get('seating_chart')
            seating.seating_chart = get_object_or_None(Image, id=imageId)
        seating.save()
        return redirect(self.success_url, username=self.user.username)

seating = SeatingView.as_view()

class StaffView(VenueProfileFormMixin, MultipleModelFormsView):
    form_classes = {
      'staffForm' : forms.StaffForm,
      'contactForm' : ContactForm
    }
    template_name = 'venue/forms_staff.html'
    model = models.Staff
    success_url = 'venue:about'
    staff_id=None

    def get_context_data(self, **kwargs):
        context = super(StaffView, self).get_context_data(**kwargs)
        staff = self.model.objects.filter(profile=self.user.profile.venueProfile)
        context['staff'] = staff
        context['staff_id'] = self.kwargs.get('staff_id', None)
        return context

    def get_objects(self, queryset=None):
        self.staff_id = self.kwargs.get('staff_id')
        staff = get_object_or_None(self.model, id=self.staff_id)
        return {
            'staffForm' : staff,
            'contactForm' : staff.contact if staff else None
        }

    def forms_valid(self, forms):
        staff = forms['staffForm'].save(commit=False, id=self.kwargs.get('staff_id'))
        if staff:
            staff.profile = self.user.profile.venueProfile
            contact = forms['contactForm'].save()
            staff.contact = contact
            staff.save()
        return redirect(self.success_url, username=self.user.username)

staff = StaffView.as_view()
