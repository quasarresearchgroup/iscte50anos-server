# Generated by Django 4.0.4 on 2023-03-14 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_trial_is_completed_alter_trialquestion_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
