"""Mixins for the API."""

import uuid

from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _


class AtomicMixin(object):
    """
    Ensure we rollback db transactions on exceptions.

    From https://gist.github.com/adamJLev/7e9499ba7e436535fd94
    """

    @transaction.atomic()
    def dispatch(self, *args, **kwargs):
        """Atomic transaction."""
        return super(AtomicMixin, self).dispatch(*args, **kwargs)

    def handle_exception(self, *args, **kwargs):
        """Handle exception with transaction rollback."""
        response = super(AtomicMixin, self).handle_exception(*args, **kwargs)

        if getattr(response, 'exception'):
            # We've suppressed the exception but still need to rollback any
            # transaction.
            transaction.set_rollback(True)

        return response


class CreateMixin(models.Model):
    """Store timestamps for creation."""

    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        abstract = True
        get_latest_by = 'created'
        ordering = ('created',)


class CreateUpdateMixin(CreateMixin):
    """Store timestamps for the last modification."""

    updated = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        abstract = True


class ValidFromUntilMixin(models.Model):
    """Valid from / until date fields."""

    valid_from_inclusive = models.DateField(
        _('valid_from'), auto_now_add=True, null=False, blank=False)
    valid_until_exclusive = models.DateField(
        _('valid until'), null=True, blank=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    """Use a UUID Field as a primary ID."""

    id = models.UUIDField(_('ID'), primary_key=True,
                          unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
