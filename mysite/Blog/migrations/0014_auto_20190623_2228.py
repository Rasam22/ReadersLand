# Generated by Django 2.2.2 on 2019-06-23 16:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20190623_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='writer',
            old_name='writerwrotethebooks',
            new_name='books',
        ),
    ]
