# Generated by Django 2.2.2 on 2019-06-24 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_auto_20190624_2108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='books',
        ),
    ]
