# Generated by Django 4.1.7 on 2023-04-05 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_event_created_event_date_event_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hackathon_participant',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
