# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogaudit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Syslog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
