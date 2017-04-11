# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-11 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iziCMSapp', '0014_site_root_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='path',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='page',
            name='selector',
            field=models.CharField(default='body', max_length=255),
        ),
        migrations.AlterField(
            model_name='site',
            name='ftp_host',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='site',
            name='ftp_user',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='site',
            name='hostname',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='root_folder',
            field=models.CharField(default='/', max_length=255),
        ),
    ]