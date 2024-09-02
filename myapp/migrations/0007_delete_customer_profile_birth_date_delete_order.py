# Generated by Django 5.1 on 2024-09-01 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_profile_address_remove_profile_city_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]