# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 03:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20171206_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='questionnaire',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app01.Questionnaire', verbose_name='所属问卷'),
        ),
    ]
