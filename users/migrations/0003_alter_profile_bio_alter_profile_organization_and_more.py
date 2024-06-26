# Generated by Django 5.0.6 on 2024-05-30 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(default='Default Bio', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='organization',
            field=models.CharField(default='Default organization', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(default='987654321', max_length=12),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work',
            field=models.CharField(default='Developer', max_length=250),
        ),
    ]
