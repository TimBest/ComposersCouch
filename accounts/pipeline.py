import string, random
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

from artist.models import ArtistProfile
from fan.models import FanProfile
from venue.models import VenueProfile
from accounts.models import Profile
from contact.models import ContactInfo, Contact
from schedule.models import Calendar


def getProfileDetails(request, backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        Part of SOCIAL_AUTH_PIPELINE. Works with django-social-auth==0.7.21 or newer
        @backend - social_auth.backends.twitter.TwitterBackend (or other) object
        @user - User (if is_new) or django.utils.functional.SimpleLazyObject (if new_association)
        @social_user - UserSocialAuth object
    """
    request.session['backend'] = backend.name
    if not hasattr(user, 'profile'):
        return redirect('/signup/social/', user=user)
    else:
        return None

def createProfile(request, backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        if user has profile skip else create new profile
    """
    if not hasattr(user, 'profile'):
        user.profile = Profile(user=user)
        user.profile.save()
        # TODO: remove this call to get profile type?
        profile_type = request.session.get('profile').profile_type
        location     = request.session.get('location')
        first_name   = request.session.get('first_name')
        last_name    = request.session.get('last_name')
        band_name    = request.session.get('band_name')
        venue_name   = request.session.get('venue_name')
        create_profile(user, profile_type, location, first_name,
                       last_name, band_name, venue_name)
    return None

def create_profile(user, profile_type, location, first_name=None, last_name=None,
                   band_name=None, venue_name=None):

    profile_type = profile_type
    if profile_type == 'f':
        # Create Fan Profile
        fan = FanProfile(profile=user.profile, user=user)
        fan.save()

        # must be after fan.save()
        user.first_name = first_name
        user.last_name = last_name
        user.username = get_username(user.first_name+user.last_name)
        user.save()

        user.profile.profile_type = 'f'
        contact = Contact(name=user.first_name+" "+user.last_name)

    elif profile_type == 'm':
        # Create Musician Profile
        artist = ArtistProfile(profile=user.profile, user=user)
        artist.name = band_name
        artist.save()
        user.username = get_username(artist.name)
        user.save()
        # must be after artist.save()
        user.profile.profile_type = 'm'
        contact = Contact(name=artist.name)

    elif profile_type == 'v':
        # Create Fan Profile
        venue = VenueProfile(profile=user.profile, user=user)
        venue.name = venue_name
        venue.save()
        user.username = get_username(venue.name)
        user.save()
        # must be after venue.save()
        user.profile.profile_type = 'v'
        contact = Contact(name=venue.name)

    location.save()
    contact.save()
    Contact_info = ContactInfo(contact=contact,location=location)
    Contact_info.save()
    user.profile.contact_info = Contact_info
    user.profile.save()
    Calendar.objects.get_or_create_calendar(user, name=user.username)
    return user


USERNAME_LENGTH = User._meta.get_field('username').max_length

def get_username(username):
    username = username.replace (" ", "_")
    username = slugify(username)[:USERNAME_LENGTH]
    try:
        User.objects.get(username=username)
        if len(username) >= USERNAME_LENGTH:
            return get_username(random.choice(string.letters+string.digits))
        else:
            return get_username(username+random.choice(string.letters+string.digits))
    except User.DoesNotExist:
        return username;
