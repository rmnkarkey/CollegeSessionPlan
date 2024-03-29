# Generated by Django 2.2.2 on 2019-07-04 06:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoAuthentication', '0006_auto_20190704_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmanagement',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 12, 3, 1, 600681)),
        ),
        migrations.AlterField(
            model_name='studentmanagement',
            name='enrolled_year',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 4, 12, 3, 1, 600681)),
        ),
        migrations.CreateModel(
            name='subfirebase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoAuthentication.FirebaseDatabase')),
            ],
        ),
    ]
