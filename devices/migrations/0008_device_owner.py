# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-29 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('devices', '0007_graphmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='owner',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.Group'),
        ),
    ]
