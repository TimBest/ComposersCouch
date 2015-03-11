from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in

from django.utils.crypto import get_random_string

from accounts.pipeline import create_profile
from accounts.models import Profile


def create_user_profile(name, email, profile_type, creator):
    user = User.objects.create_user(username=get_random_string(), email=email)
    # apparently django does not let you reset a password if one is not initally set
    user.set_password(get_random_string())
    user.save()
    user.profile = Profile(user=user)
    user.profile.save()
    location = creator.profile.contact_info.location
    location.pk = None
    location.save()
    user = create_profile(user=user, profile_type=profile_type,
                          location=location, band_name=name, venue_name=name)
    user.profile.has_owner=False
    user.profile.save()
    return user

def update_profile_weight(sender=None, user=None, request=None, **kwargs):
    """
        # mugshot = 100
        # biography = 50
        # email = 25
    """
    weight = 0
    # mugshot
    if user.profile.mugshot:
        weight = weight + 100
    # biography
    if user.profile.profile_type == 'm':
        if user.profile.artist_profile.biography:
            weight = weight + 50
    elif user.profile.profile_type == 'm':
        if user.profile.venueProfile.biography:
            weight = weight + 50
    # email
    if user.email:
        weight = weight + 25
    user.profile.weight = weight
    user.profile.save()

user_logged_in.connect(update_profile_weight)

def update_profiles():
    """ update the weight of all profiles """
    for profile in Profile.objects.all():
        update_profile_weight(user=profile.user)
