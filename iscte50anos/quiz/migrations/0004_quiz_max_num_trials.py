# Generated by Django 4.1 on 2023-04-13 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_question_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='max_num_trials',
            field=models.IntegerField(default=3),
        ),
    ]
