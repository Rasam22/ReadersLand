# Generated by Django 2.2.2 on 2019-06-29 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0036_book_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='buying_link',
            field=models.CharField(default='link', max_length=500),
        ),
    ]
