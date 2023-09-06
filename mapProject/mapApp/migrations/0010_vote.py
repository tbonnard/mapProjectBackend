# Generated by Django 4.2.4 on 2023-08-29 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0009_property_with_suggestions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voteFromProject', to='mapApp.project')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voteFromProperty', to='mapApp.property')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voteFromUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]