# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-15 01:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_auto_20170415_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookstar',
            old_name='content',
            new_name='rating',
        ),
    ]
