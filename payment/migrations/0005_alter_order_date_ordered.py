# Generated by Django 5.1 on 2024-08-31 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_rename_email_order_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]