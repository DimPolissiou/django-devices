# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_auto_20161113_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='django_netjsonconfig.Config'),
        ),
        migrations.AlterField(
            model_name='device',
            name='geom',
            field=djgeojson.fields.PolygonField(),
        ),
    ]
