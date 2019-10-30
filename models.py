from django.db import models
from django.contrib.postgres.fields import ArrayField
from .settings import *

# Create your models here.


class ProdCals(models.Model):
    locale = models.CharField(
        'Локализация',
        max_length=2,
        choices=LOCALE_SUPPORTING,
        default=DEFAULT_LOCALE,
        null=False,
        blank=False,
    )
    year = models.PositiveSmallIntegerField('Год', null=False, blank=False)
    dates = ArrayField(models.DateField(), default=list)

    class Meta:
        db_table = 'prodcal_prodcals'
        verbose_name = 'Производственный календарь'
        verbose_name_plural = 'Производственный календарь'




