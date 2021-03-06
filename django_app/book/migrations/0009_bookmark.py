# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-17 23:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_auto_20170416_0515'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('mybook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.MyBook')),
            ],
        ),
    ]
