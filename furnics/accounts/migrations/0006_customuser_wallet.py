# Generated by Django 4.2.4 on 2023-11-06 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='wallet',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
