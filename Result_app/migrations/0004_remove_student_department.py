# Generated by Django 5.0.1 on 2024-06-30 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Result_app', '0003_student_education'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='department',
        ),
    ]
