# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bitfield.models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_category_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('flags', bitfield.models.BitField(((b'awesome_flag', b'Awesome Flag!'), (b'flaggy_foo', b'Flaggy Foo'), (b'baz_bar', b'Baz (bar)')), default=None)),
            ],
        ),
    ]
