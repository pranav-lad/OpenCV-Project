# -*- coding: utf-8 -*-

__version__ = '0.1.0'

from django.contrib.admin import SimpleListFilter
from django.utils.translation import ugettext_lazy as _


def isnull_filter(field_name, filter_title=None):
    class HasRelatedFieldFilter(SimpleListFilter):
        parameter_name = '%s__isnull' % field_name
        related_field = field_name

        def __init__(self, request, field, model, model_admin):
            related_field = model._meta.get_field(field_name)
            if filter_title:
                self.title = filter_title
            else:
                if hasattr(related_field, 'related'):
                    related_title = related_field.related.model._meta.verbose_name_plural
                    self.title = _("Is related '%s' null?") % related_title
                elif hasattr(related_field, 'related_model') and hasattr(related_field.related_model, "_meta"):
                    related_title = related_field.related_model._meta.verbose_name_plural
                    self.title = _("Is related '%s' null?") % related_title
                else:
                    related_title = related_field.name
                    self.title = _("Is field '%s' null?") % related_title
            super(HasRelatedFieldFilter, self).__init__(request, field, model, model_admin)

        def lookups(self, request, model_admin):
            return [
                ('true', _('True')),
                ('false', _('False')),
            ]

        def queryset(self, request, queryset):
            kwargs = {}
            if self.value() in ('false', 'False'):
                kwargs["%s__isnull" % self.related_field] = False
            if self.value() in ('true', 'True'):
                kwargs["%s__isnull" % self.related_field] = True
            return queryset.filter(**kwargs).distinct()

    return HasRelatedFieldFilter
