# Generated by Django 4.2.6 on 2024-05-07 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0028_remove_salestransaction_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salestransaction',
            name='mobile_number',
            field=models.CharField(max_length=10),
        ),
    ]
