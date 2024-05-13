# Generated by Django 4.2.6 on 2024-05-04 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_salestransaction_address_salestransaction_items_sold_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesitem',
            old_name='inventory_item',
            new_name='product',
        ),
        migrations.RenameField(
            model_name='salesitem',
            old_name='quantity_sold',
            new_name='quantity',
        ),
        migrations.AddField(
            model_name='salesitem',
            name='gst',
            field=models.DecimalField(decimal_places=2, default=4, max_digits=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salesitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
    ]