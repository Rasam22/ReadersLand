# Generated by Django 2.2.2 on 2019-06-25 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20190626_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_image',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
