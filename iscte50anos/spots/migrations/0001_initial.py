# Generated by Django 4.0.4 on 2022-08-08 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LayoutPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100)),
                ('start_date', models.DateField(blank=True)),
                ('end_date', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField()),
                ('topic', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='topics.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100)),
                ('location_photo_link', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='QRCodeAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_accessed', models.BooleanField(default=False)),
                ('access_date', models.DateTimeField(auto_now=True)),
                ('qrcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spots.qrcode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Layout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spots.layoutperiod')),
                ('qrcode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spots.qrcode')),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='spots.spot')),
            ],
        ),
    ]