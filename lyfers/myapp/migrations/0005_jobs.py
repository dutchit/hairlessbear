# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_providerprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=200)),
                ('date', models.DateField()),
                ('duration', models.IntegerField()),
                ('timeUnit', models.CharField(blank=True, max_length=200)),
                ('price', models.CharField(blank=True, max_length=5)),
                ('lowerBound', models.IntegerField()),
                ('upperBound', models.IntegerField()),
                ('username', models.ForeignKey(to='myapp.UserProfile')),
            ],
        ),
    ]
