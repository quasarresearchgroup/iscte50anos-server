# Generated by Django 4.0.1 on 2022-03-07 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_alter_question_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trial',
            old_name='num_trial',
            new_name='number',
        ),
        migrations.AddField(
            model_name='trial',
            name='current_question',
            field=models.IntegerField(default=0),
        ),
    ]
