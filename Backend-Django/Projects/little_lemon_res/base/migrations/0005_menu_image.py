# Generated by Django 4.1.3 on 2023-02-11 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_booking_description_menu_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='menu_items/'),
        ),
    ]
