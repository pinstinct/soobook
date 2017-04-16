# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 13:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_auto_20170415_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookstar',
            name='content',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]