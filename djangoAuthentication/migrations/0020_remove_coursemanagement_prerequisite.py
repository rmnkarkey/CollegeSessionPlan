# Generated by Django 2.2.2 on 2019-08-05 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoAuthentication', '0019_prerequisite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemanagement',
            name='prerequisite',
        ),
    ]
