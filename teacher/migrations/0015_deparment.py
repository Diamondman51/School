# Generated by Django 5.1.1 on 2024-09-28 18:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0014_alter_score_attendance_mark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deparment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, null=True, unique=True)),
                ('email', models.EmailField(max_length=100)),
                ('starting_year', models.DateField()),
                ('student_capacity', models.IntegerField()),
                ('head_of_department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]