# Generated by Django 2.2.2 on 2019-08-05 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoAuthentication', '0018_auto_20190805_0938'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prerequisite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_course_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='main_name', to='djangoAuthentication.CourseManagement')),
                ('main_course_pre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='preq_name', to='djangoAuthentication.CourseManagement')),
            ],
        ),
    ]
