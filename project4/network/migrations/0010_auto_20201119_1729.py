# Generated by Django 3.1.1 on 2020-11-19 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20201116_1519'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posts',
            old_name='likes',
            new_name='totallikes',
        ),
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(related_name='fans', to='network.Posts'),
        ),
    ]
