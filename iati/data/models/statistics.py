# Django specific
from django.db import models


class ActivityStatistics(models.Model):
    iati_identifier = models.CharField(max_length=50, primary_key=True)
    total_budget = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        app_label = "data"
