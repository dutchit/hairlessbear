# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20150921_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('profileTitle', models.CharField(max_length=200, blank=True)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(max_length=200, blank=True)),
                ('username', models.ForeignKey(to='myapp.UserProfile')),
            ],
        ),
    ]
