# Generated by Django 5.1.2 on 2025-02-09 19:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0023_alter_group_name_alter_group_read_more_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.groupspec'),
        ),
        migrations.AlterField(
            model_name='group',
            name='read_more',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.readmore'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grouplikes',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.group'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.group'),
        ),
        migrations.AlterField(
            model_name='lessonfiles',
            name='lesson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.lesson'),
        ),
        migrations.AlterField(
            model_name='score_attendance',
            name='lesson',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.lesson'),
        ),
        migrations.AlterField(
            model_name='score_attendance',
            name='student',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.student'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='department',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='teacher.groupspec'),
        ),
    ]
