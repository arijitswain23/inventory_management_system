# Generated by Django 4.2.6 on 2024-05-08 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0031_alter_salestransaction_sale_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
