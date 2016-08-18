# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160727_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('action', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
