# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-17 08:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_remove_plan_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
