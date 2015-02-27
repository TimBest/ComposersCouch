from django.contrib.auth.models import User
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
