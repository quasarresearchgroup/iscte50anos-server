# Generated by Django 4.0.4 on 2022-08-08 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('type', models.CharField(choices=[('student', 'Student'), ('professor', 'Professor'), ('researcher', 'Researcher'), ('staff', 'Staff')], default='student', max_length=10)),
                ('cycle', models.CharField(choices=[('bsc', "Bachelor's"), ('msc', "Master's"), ('phd', 'Doctorate')], max_length=3)),
                ('subtype', models.CharField(blank=True, max_length=50)),
                ('abbreviation', models.CharField(blank=True, max_length=30)),
                ('full_description', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('percent_correct', models.DecimalField(decimal_places=2, max_digits=3)),
                ('min_topics', models.IntegerField()),
                ('max_topics', models.IntegerField()),
                ('trials_allowed', models.IntegerField()),
                ('max_points_quiz', models.IntegerField()),
                ('max_time_per_question', models.IntegerField()),
                ('num_single_questions', models.IntegerField()),
                ('num_multiple_questions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('points', models.IntegerField(default=0)),
                ('num_spots_read', models.IntegerField(default=0)),
                ('total_time', models.IntegerField(default=0)),
                ('is_logged', models.BooleanField(default=False)),
                ('affiliation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.affiliation')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['num_spots_read', '-total_time'], name='users_profi_num_spo_04c653_idx'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['points'], name='users_profi_points_da4051_idx'),
        ),
    ]
