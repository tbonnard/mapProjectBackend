# Generated by Django 4.2.4 on 2023-08-29 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0010_vote'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='vote',
            constraint=models.UniqueConstraint(fields=('voter', 'project', 'value'), name='unique_voter_property_value_combination'),
        ),
    ]
