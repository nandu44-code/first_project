# Generated by Django 4.2.4 on 2023-11-13 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_name', models.CharField(max_length=50)),
                ('banner_image', models.ImageField(default=None, upload_to='photos/banner/')),
            ],
        ),
    ]