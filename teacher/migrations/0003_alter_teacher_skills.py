# Generated by Django 5.1.1 on 2024-09-25 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_teacher_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='skills',
            field=models.ManyToManyField(blank=True, to='teacher.skill'),
        ),
    ]