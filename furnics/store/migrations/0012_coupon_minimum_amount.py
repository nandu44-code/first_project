# Generated by Django 4.2.4 on 2023-11-10 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='minimum_amount',
            field=models.IntegerField(default=500),
        ),
    ]
