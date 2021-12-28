from django.db.models import Manager, QuerySet
from django.utils import timezone


class BaseManager(Manager):
    def __init__(self, *args, **kwargs):
        self.this_year_lookup = kwargs.pop('this_year_lookup',
                                           'created_on__year')
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        return BaseManagerQuerySet(self.model,
                                   using=self._db,
                                   this_year_lookup=self.this_year_lookup)

    def from_year(self, year, *ar, **kw):
        return self.get_queryset().from_year(year, *ar, **kw)

    def this_year(self, *ar, **kw):
        return self.get_queryset().this_year(*ar, **kw)


class BaseManagerQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        self.this_year_lookup = kwargs.pop('this_year_lookup',
                                           'created_on__year')
        super().__init__(*args, **kwargs)

    def from_year(self, year):
        return self.filter(**{self.this_year_lookup: year})

    def this_year(self):
        return self.filter(**{self.this_year_lookup: timezone.now().year})
