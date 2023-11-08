# Generated by Django 4.2.4 on 2023-11-06 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_userwallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwallet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
