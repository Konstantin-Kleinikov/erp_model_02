from django.db import models

from core.models import AuditTrailModel, NoteModel


class Currency(AuditTrailModel, NoteModel):
    code = models.CharField(
        primary_key=True,
        max_length=3,
        unique=True,
        null=False,
        verbose_name='Currency Code',
    )
    name = models.CharField(
        max_length=30,
        verbose_name='Short Description',
    )
    iso_code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name='ISO',
    )
    numeric_code = models.PositiveSmallIntegerField(
        default=0,
    )

    class Meta:
        ordering = ['code']
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code
