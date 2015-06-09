from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from accounts.models import Profile
from userena.models import UserenaSignup
from userena import settings as userena_settings

class UserenaSignupInline(admin.StackedInline):
    model = UserenaSignup
    max_num = 1

class UserenaAdmin(UserAdmin):
    inlines = [UserenaSignupInline, ]
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')


if userena_settings.USERENA_REGISTER_USER:
    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        pass

    admin.site.register(User, UserenaAdmin)

if userena_settings.USERENA_REGISTER_PROFILE:
    admin.site.register(Profile)
