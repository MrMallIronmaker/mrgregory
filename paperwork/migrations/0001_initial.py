# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-01 09:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClientInfoType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Deadline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offset', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Deliverable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ClientInfoDate',
            fields=[
                ('clientinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paperwork.ClientInfo')),
                ('date', models.DateField()),
            ],
            bases=('paperwork.clientinfo',),
        ),
        migrations.CreateModel(
            name='FinalDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paperwork.Deadline')),
                ('relative_info_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.ClientInfoType')),
            ],
            bases=('paperwork.deadline',),
        ),
        migrations.CreateModel(
            name='StepDeadline',
            fields=[
                ('deadline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='paperwork.Deadline')),
                ('ancestor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='paperwork.Deadline')),
                ('deliverable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.Deliverable')),
            ],
            bases=('paperwork.deadline',),
        ),
        migrations.AddField(
            model_name='clientinfo',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.Client'),
        ),
        migrations.AddField(
            model_name='clientinfo',
            name='info_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paperwork.ClientInfoType'),
        ),
        migrations.AddField(
            model_name='deliverable',
            name='final',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paperwork.FinalDeadline'),
        ),
    ]
