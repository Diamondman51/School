# Generated by Django 5.1.2 on 2025-02-10 04:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0024_alter_group_name_alter_group_read_more_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='read_more',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.readmore'),
        ),
    ]
