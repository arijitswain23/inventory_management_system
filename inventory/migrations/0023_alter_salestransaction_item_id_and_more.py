# Generated by Django 4.2.6 on 2024-05-03 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_delete_customer_alter_salestransaction_items_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salestransaction',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventoryitem'),
        ),
        migrations.AlterField(
            model_name='salestransaction',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
