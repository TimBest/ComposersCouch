from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

from userena import settings as userena_settings
from userena.utils import generate_sha1, get_datetime_now
from userena import signals as userena_signals


import re

SHA1_RE = re.compile('^[a-f0-9]{40}$')

ASSIGNED_PERMISSIONS = {
    'profile':
        (('view_profile', 'Can view profile'),
         ('change_profile', 'Can change profile'),
         ('delete_profile', 'Can delete profile')),
    'user':
        (('change_user', 'Can change user'),
         ('delete_user', 'Can delete user'))
}

class UserenaManager(UserManager):
    """ Extra functionality for the Userena model. """

    def create_user(self, username, email, password, active=False,
                    send_email=False):
        """
        A simple wrapper that creates a new :class:`User`.

        :param username:
            String containing the username of the new user.

        :param email:
            String containing the email address of the new user.

        :param password:
            String containing the password for the new user.

        :param active:
            Boolean that defines if the user requires activation by clicking
            on a link in an e-mail. Defaults to ``False``.

        :return: :class:`User` instance representing the new user.

        """
        new_user = User.objects.create_user(
            username, email, password)
        new_user.is_active = active
        new_user.save()

        self.create_userena_profile(new_user)

        # All users have an empty profile
        from accounts.models import Profile
        try:
            new_profile = new_user.profile
        except Profile.DoesNotExist:
            new_profile = Profile(user=new_user)
            new_profile.save(using=self._db)

        return new_user

    def create_userena_profile(self, user):
        """
        Creates an :class:`UserenaSignup` instance for this user.

        :param user:
            Django :class:`User` instance.

        :return: The newly created :class:`UserenaSignup` instance.

        """
        if isinstance(user.username, unicode):
            user.username = user.username.encode('utf-8')
        salt, activation_key = generate_sha1(user.username)

        return self.create(user=user,
                           activation_key=activation_key)

    def reissue_activation(self, activation_key):
        """
        Creates a new ``activation_key`` resetting activation timeframe when
        users let the previous key expire.

        :param activation_key:
            String containing the secret SHA1 activation key.

        """
        try:
            userena = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False
        try:
            salt, new_activation_key = generate_sha1(userena.user.username)
            userena.activation_key = new_activation_key
            userena.save(using=self._db)
            userena.user.date_joined = get_datetime_now()
            userena.user.save(using=self._db)
            userena.send_activation_email()
            return True
        except Exception:
            return False

    def activate_user(self, activation_key):
        """
        Activate an :class:`User` by supplying a valid ``activation_key``.

        If the key is valid and an user is found, activates the user and
        return it. Also sends the ``activation_complete`` signal.

        :param activation_key:
            String containing the secret SHA1 for a valid activation.

        :return:
            The newly activated :class:`User` or ``False`` if not successful.

        """
        if SHA1_RE.search(activation_key):
            try:
                userena = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not userena.activation_key_expired():
                userena.activation_key = userena_settings.USERENA_ACTIVATED
                user = userena.user
                user.is_active = True
                userena.save(using=self._db)
                user.save(using=self._db)

                # Send the activation_complete signal
                userena_signals.activation_complete.send(sender=None,
                                                         user=user)

                return user
        return False

    def check_expired_activation(self, activation_key):
        """
        Check if ``activation_key`` is still valid.

        Raises a ``self.model.DoesNotExist`` exception if key is not present or
         ``activation_key`` is not a valid string

        :param activation_key:
            String containing the secret SHA1 for a valid activation.

        :return:
            True if the ket has expired, False if still valid.

        """
        if SHA1_RE.search(activation_key):
            userena = self.get(activation_key=activation_key)
            return userena.activation_key_expired()
        raise self.model.DoesNotExist

    def confirm_email(self, confirmation_key):
        """
        Confirm an email address by checking a ``confirmation_key``.

        A valid ``confirmation_key`` will set the newly wanted e-mail
        address as the current e-mail address. Returns the user after
        success or ``False`` when the confirmation key is
        invalid. Also sends the ``confirmation_complete`` signal.

        :param confirmation_key:
            String containing the secret SHA1 that is used for verification.

        :return:
            The verified :class:`User` or ``False`` if not successful.

        """
        if SHA1_RE.search(confirmation_key):
            try:
                userena = self.get(email_confirmation_key=confirmation_key,
                                   email_unconfirmed__isnull=False)
            except self.model.DoesNotExist:
                return False
            else:
                user = userena.user
                old_email = user.email
                user.email = userena.email_unconfirmed
                userena.email_unconfirmed, userena.email_confirmation_key = '',''
                userena.save(using=self._db)
                user.save(using=self._db)

                # Send the confirmation_complete signal
                userena_signals.confirmation_complete.send(sender=None,
                                                           user=user,
                                                           old_email=old_email)

                return user
        return False

    def delete_expired_users(self):
        """
        Checks for expired users and delete's the ``User`` associated with
        it. Skips if the user ``is_staff``.

        :return: A list containing the deleted users.

        """
        deleted_users = []
        for user in User.objects.filter(is_staff=False,
                                                    is_active=False):
            if user.userena_signup.activation_key_expired():
                deleted_users.append(user)
                user.delete()
        return deleted_users

class UserenaBaseProfileManager(models.Manager):
    """ Manager for :class:`UserenaProfile` """
    def get_visible_profiles(self, user=None):
        """
        Returns all the visible profiles available to this user.

        For now keeps it simple by just applying the cases when a user is not
        active, a user has it's profile closed to everyone or a user only
        allows registered users to view their profile.

        :param user:
            A Django :class:`User` instance.

        :return:
            All profiles that are visible to this user.

        """
        profiles = self.all()

        filter_kwargs = {'user__is_active': True}

        profiles = profiles.filter(**filter_kwargs)
        if user and isinstance(user, AnonymousUser):
            profiles = profiles.exclude(Q(privacy='closed') | Q(privacy='registered'))
        else: profiles = profiles.exclude(Q(privacy='closed'))
        return profiles
