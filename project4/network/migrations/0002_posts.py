# Generated by Django 3.1.1 on 2020-10-12 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=300)),
                ('date', models.DateTimeField()),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]
