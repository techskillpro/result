# Generated by Django 5.0.1 on 2024-07-01 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Result_app', '0010_course_result_semester_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester_result',
            name='department',
        ),
    ]