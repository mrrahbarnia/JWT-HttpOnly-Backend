# Generated by Django 5.0.6 on 2024-07-06 15:23

import users.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='security_stamp',
            field=models.CharField(blank=True, default=users.models.default_security_stamp, null=True),
        ),
    ]
