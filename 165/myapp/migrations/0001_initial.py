# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('profileTitle', models.CharField(blank=True, max_length=202)),
                ('location', models.CharField(blank=True, max_length=202)),
                ('description', models.TextField()),
                ('token', models.CharField(blank=True, max_length=220)),
                ('username', models.CharField(blank=True, max_length=220)),
                ('displayName', models.CharField(max_length=200)),
                ('first_name', models.CharField(blank=True, max_length=220)),
                ('last_name', models.CharField(blank=True, max_length=220)),
                ('password', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
