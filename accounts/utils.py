from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from pipeline import create_profile
from models import Profile


def create_user_profile(name, email, profile_type, creator):
    user = User.objects.create_user(username=get_random_string(), email=email)
    # apparently django does not let you reset a password if one is not initally set
    user.set_password(get_random_string())
    user.save()
    profile = Profile(user=user, has_owner=False, profile_type=profile_type)
    profile.save()
    location = creator.profile.contact_info.location
    location.pk = None
    location.save()
    return create_profile(user=user, profile_type=profile_type,
                          location=location, band_name=name, venue_name=name)
