# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-06 11:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='caption',
            field=models.TextField(max_length=64, verbose_name='问题'),
        ),
    ]
