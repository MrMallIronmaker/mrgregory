# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-11 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paperwork', '0007_taskstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('completed', models.BooleanField()),
                ('deadline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.Deadline')),
                ('task_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.TaskStatus')),
            ],
        ),
        migrations.AlterField(
            model_name='clientinfotypesignature',
            name='deliverable',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paperwork.Deliverable'),
        ),
    ]