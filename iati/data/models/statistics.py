# Django specific
from django.db import models

# Data specific
from data.models.activity import IATIActivity
from data.models.organisation import Organisation


class ActivityStatistics(models.Model):
    iati_identifier = models.OneToOneField(IATIActivity)
    total_budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = "data"
