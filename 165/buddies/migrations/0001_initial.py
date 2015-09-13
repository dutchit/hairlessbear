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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('profileTitle', models.TextField()),
                ('location', models.TextField()),
                ('description', models.TextField()),
                ('token', models.TextField()),
                ('username', models.TextField()),
                ('displayName', models.CharField(max_length=200)),
                ('first_name', models.TextField()),
                ('last_name', models.TextField()),
                ('password', models.CharField(blank=True, max_length=20)),
            ],
        ),
    ]
