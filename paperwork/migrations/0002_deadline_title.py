# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-01 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deadline',
            name='title',
            field=models.CharField(default='ded', max_length=200),
            preserve_default=False,
        ),
    ]
