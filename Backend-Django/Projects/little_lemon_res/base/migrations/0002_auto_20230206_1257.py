# Generated by Django 3.2.12 on 2023-02-06 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Employees',
        ),
        migrations.DeleteModel(
            name='Reservation',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='comments',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='guest_count',
            new_name='guest_number',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='reservation_time',
        ),
    ]
