# Generated by Django 2.2.2 on 2019-08-09 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoAuthentication', '0028_auto_20190809_0752'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursemanagement',
            unique_together={('course_code', 'session')},
        ),
    ]
