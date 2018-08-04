import uuid
from datetime import timedelta

from allauth.account.models import EmailAddress

from django.conf import settings
from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from server.helpers.models.mixins import UUIDMixin
from server.apps.tenants.models import Tenant


class UserManager(BaseUserManager):
    use_in_migrations = True

    def find_next_available_username(self, wanted_username):
        counter = 1
        checked_username = wanted_username

        while True:

            try:
                self.model.objects.get(username=checked_username)
            except self.model.DoesNotExist:
                return checked_username

            counter += 1

            checked_username = "{}{}".format(wanted_username, counter)

    def _create_user(self, email, password, username=None, **extra_fields):
        """Create and save a User with the given credentials."""
        if email is None:
            raise ValueError('The email must be set')

        email = self.normalize_email(email)

        if username is None or username == '':
            username = self.find_next_available_username(email.split("@")[0])

        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(email, password, username, **extra_fields)

    def create_superuser(self, email, password, username=None, **extra_fields):

        if password is None:
            raise TypeError('Superusers must have a password.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_instance_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        superuser = self._create_user(
            email, password, username, **extra_fields)

        # (Force-)Verify email of superuser
        verification, created = EmailAddress.objects.get_or_create(
            user=superuser, email=superuser.email)
        verification.verified = True
        verification.set_as_primary()
        verification.save()

        return superuser


class User(AbstractBaseUser, UUIDMixin, PermissionsMixin):

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female')
    )

    email = models.EmailField(
        _('email address'),
        help_text=_("Email of the user"),
        null=False,
        blank=False,
        unique=True
    )

    confirmed_email = models.BooleanField(default=False)

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            '150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    first_name = models.CharField(
        _('first name'),
        help_text=_("First Name of the user"),
        max_length=30,
        blank=True
    )

    last_name = models.CharField(
        _('last name'),
        max_length=30,
        blank=True,
        help_text=_("Last Name of the user")
    )

    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=GENDER_MALE)

    activation_key = models.UUIDField(unique=True, default=uuid.uuid4)

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )

    is_superuser = models.BooleanField(_('superuser status'), default=False)

    is_instance_admin = models.BooleanField(
        _('tenant admin status'), default=False)

    date_joined = models.DateTimeField(_('date joined'), help_text=_(
        "When did the user join?"), default=timezone.now)

    signed_in = models.DateTimeField(
        _('Signed in'), help_text=_("Is the user signed in?"), null=True)

    tenants = models.ManyToManyField(
        Tenant,
        help_text=_("Where is the user registered?"),
        through='UserTenantRelationship'
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return f"admin/users/user/{self.id}/change/"

    def activation_expired(self):
        """
        Check if user's activation has expired.

        :return: boolean
        """
        return self.date_joined + timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS) < timezone.now()

    def confirm_email(self):
        """
        Confirm email.

        :return: boolean
        """
        if not self.activation_expired() and not self.confirmed_email:
            self.confirmed_email = True
            self.save()
            return True
        return False


class UserTenantRelationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.tenant)

    class Meta:
        verbose_name = _('employment')
        verbose_name_plural = _('employments')


@receiver(user_logged_in)
def on_user_login(sender, **kwargs):
    user = kwargs.get('user')
    user.signed_in = timezone.now()
    user.save()


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    user = kwargs.get('user')
    # Do not process anonymous users
    if user:
        user.signed_in = None
        user.save()
