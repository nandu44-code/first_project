# Generated by Django 4.2.4 on 2023-11-13 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='banner_count',
            field=models.IntegerField(default=1),
        ),
    ]
