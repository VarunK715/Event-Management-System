# Generated by Django 5.0.6 on 2024-05-30 12:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_ems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 5, 30, 12, 3, 24, 859491, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]