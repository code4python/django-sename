# Generated by Django 4.2.3 on 2023-07-21 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sename', '0003_rename_hell_movie_hall'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='date',
        ),
    ]
