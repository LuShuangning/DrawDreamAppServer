# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-26 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsdetail',
            name='nede_cover_img',
            field=models.URLField(default=''),
        ),
    ]
