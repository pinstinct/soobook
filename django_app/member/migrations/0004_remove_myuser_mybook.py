# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 01:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_myuser_mybook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='mybook',
        ),
    ]