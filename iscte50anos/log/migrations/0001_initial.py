# Generated by Django 4.0.4 on 2022-12-02 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_ip', models.CharField(max_length=15)),
                ('link', models.CharField(max_length=100)),
                ('access_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
