# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_jobs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='duration',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='lowerBound',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='upperBound',
            field=models.IntegerField(blank=True),
        ),
    ]
