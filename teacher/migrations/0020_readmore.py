# Generated by Django 5.1.2 on 2025-02-09 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0019_group_course_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadMore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_course', models.TextField(blank=True, null=True)),
                ('course_info', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Read More',
            },
        ),
    ]
