# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20150921_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='displayName',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
