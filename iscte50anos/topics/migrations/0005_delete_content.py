# Generated by Django 4.0.1 on 2022-03-02 20:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_content_date_content_scope'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Content',
        ),
    ]