import string, random
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.defaultfilters import slugify

from guardian.shortcuts import assign_perm

from models import Profile, FanProfile, MusicianProfile, VenueProfile
from accounts,models import Profile
from annoying.functions import get_object_or_None
from contact.models import ContactInfo, Contact, Location, Zipcode
from schedule.models import Calendar
import userena.managers


def getProfileDetails(request, backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        Part of SOCIAL_AUTH_PIPELINE. Works with django-social-auth==0.7.21 or newer
        @backend - social_auth.backends.twitter.TwitterBackend (or other) object
        @user - User (if is_new) or django.utils.functional.SimpleLazyObject (if new_association)
        @social_user - UserSocialAuth object
    """
    request.session['backend'] = backend.name
    try:
        profile = user.profile
    except:
        return redirect('/signup/social/', user=user)
    return None

def createProfile(request, backend, user, social_user, is_new=False, new_association=False, *args, **kwargs):
    """
        if user has profile skip else create new profile
    """
    try:
        profile = user.profile
    except:
        profile = Profile(user=user)
        profile.save()
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

    profile = user.profile
    # Give permissions to view and change profile
    for perm in userena.managers.ASSIGNED_PERMISSIONS['profile']:
        assign_perm(perm[0], user, profile)

    # Give permissions to view and change itself
    for perm in userena.managers.ASSIGNED_PERMISSIONS['user']:
        assign_perm(perm[0], user, user)

    profile_type = profile_type
    if(profile_type == 'f'):
        # Create Fan Profile
        fan = FanProfile(profile = profile, user=user)
        fan.save()

        # must be after fan.save()
        user.first_name = first_name
        user.last_name = last_name
        user.username = get_username(user.first_name+user.last_name)
        user.save()

        profile.profile_type = 'f'
        contact = Contact(name=user.first_name+" "+user.last_name)

    elif(profile_type == 'm'):
        # Create Musician Profile
        musician = MusicianProfile(profile = profile, user = user)
        musician.name = band_name
        musician.save()
        user.username = get_username(musician.name)
        user.save()
        # must be after musician.save()
        profile.profile_type = 'm'
        contact = Contact(name=musician.name)

    elif(profile_type == 'v'):
        # Create Fan Profile
        venue = VenueProfile(profile = profile, user=user)
        venue.name = venue_name
        venue.save()
        user.username = get_username(venue.name)
        user.save()
        # must be after venue.save()
        profile.profile_type = 'v'
        contact = Contact(name=venue.name)

    contact.save()
    Contact_info = ContactInfo(contact=contact,location=location)
    Contact_info.save()
    profile.contact_info = Contact_info
    profile.save()
    calendar = Calendar.objects.get_or_create_calendar(user, name = user.username)
    return user

def get_username(username):
    username = username.replace (" ", "_")
    username = slugify(username)
    try:
        User.objects.get(username=username)
        return get_username(username+'_'+random.choice(string.letters))
    except User.DoesNotExist:
        return username;
