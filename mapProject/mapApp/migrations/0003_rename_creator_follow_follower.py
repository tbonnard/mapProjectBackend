# Generated by Django 4.2.4 on 2023-08-25 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0002_follow'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='creator',
            new_name='follower',
        ),
    ]
