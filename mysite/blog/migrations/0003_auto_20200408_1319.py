# Generated by Django 2.1.7 on 2020-04-08 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200408_1216'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='phoneNumber',
        ),
        migrations.AddField(
            model_name='signup',
            name='password',
            field=models.CharField(default='123456', max_length=20),
        ),
    ]
