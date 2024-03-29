# Generated by Django 4.0.4 on 2022-08-08 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('topics', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(blank=True, null=True)),
                ('scope', models.CharField(choices=[('iscte', 'Iscte'), ('portugal', 'Portugal'), ('world', 'World')], default='iscte', max_length=12)),
                ('content', models.ManyToManyField(related_name='events', to='content.content')),
                ('topics', models.ManyToManyField(related_name='events', to='topics.topic')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
    ]
