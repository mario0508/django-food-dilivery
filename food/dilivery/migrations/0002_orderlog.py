# Generated by Django 3.0.2 on 2020-02-03 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dilivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=150)),
                ('seller', models.CharField(max_length=150)),
                ('order', models.CharField(max_length=10000)),
                ('total', models.IntegerField()),
            ],
        ),
    ]
