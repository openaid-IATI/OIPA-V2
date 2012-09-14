# Django specific
from django.db import models

# Data specific
from data.models.activity import IATIActivity
from data.models.common import Country
from data.models.organisation import Organisation


class ActivityStatistics(models.Model):
    iati_identifier = models.OneToOneField(IATIActivity)
    total_budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = "data"


class CountryStatistics(models.Model):
    country = models.OneToOneField(Country)
    total_activities = models.IntegerField(default=0)

    class Meta:
        app_label = "data"


class OrganisationStatistics(models.Model):
    organisation = models.OneToOneField(Organisation)
    total_activities = models.IntegerField(default=0)

    class Meta:
        app_label = "data"


