# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-05 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20161004_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='notspam',
            name='source',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='spam',
            name='source',
            field=models.CharField(default='', max_length=50),
        ),
    ]
