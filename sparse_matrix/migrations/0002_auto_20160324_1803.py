# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-24 18:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sparse_matrix', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sparse',
            old_name='processing_time',
            new_name='processing_time_c',
        ),
        migrations.AddField(
            model_name='sparse',
            name='processing_time_l',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sparse',
            name='processing_time_q',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
