# Generated by Django 3.1.1 on 2020-11-20 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_auto_20201119_1729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(related_name='fans', to='network.Posts'),
        ),
    ]