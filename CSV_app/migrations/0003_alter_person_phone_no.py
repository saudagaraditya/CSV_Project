# Generated by Django 4.2.7 on 2023-11-24 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CSV_app', '0002_remove_person_phone_number_person_phone_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone_no',
            field=models.CharField(max_length=15),
        ),
    ]
