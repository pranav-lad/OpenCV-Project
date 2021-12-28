""" Something here """

from uuid import uuid4

from django.db import models
from django.utils.translation import ugettext_lazy as _

from meeting.common.managers import BaseManager


__all__ = ['NamedBaseModel']


class BaseModel(models.Model):
    objects = BaseManager(this_year_lookup='created_on__year')

    created_on = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Criado em'))

    modified_on = models.DateTimeField(auto_now=True,
                                       verbose_name=_('Modificado em '))

    class Meta:
        abstract = True
        ordering = ('created_on', )


class NamedBaseModel(BaseModel):
    """Named Something"""

    name = models.CharField(
        max_length=100,
        verbose_name=_('Nome'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PersonModel(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Nome'),
    )

    document = models.CharField(
        max_length=100,
        verbose_name=_('Documento'),
    )

    note = models.TextField(
        blank=True,
        verbose_name=_('Nota')
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RawUUIDModel(models.Model):
    uuid = models.CharField(
        blank=True,
        db_index=True,
        null=True,
        max_length=36,
        unique=True,
        editable=False,
        verbose_name=_('QRCode'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.uuid

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid4())
        return super().save(*args, **kwargs)
