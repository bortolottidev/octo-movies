# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-10 17:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recensioni', '0014_auto_20171110_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recensione',
            name='nclicks',
            field=models.IntegerField(default=0),
        ),
    ]