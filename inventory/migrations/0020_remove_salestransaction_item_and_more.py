# Generated by Django 4.2.6 on 2024-05-03 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_remove_salestransaction_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salestransaction',
            name='item',
        ),
        migrations.AddField(
            model_name='salestransaction',
            name='item_id',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, related_name='sales_transactions_as_item', to='inventory.inventoryitem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salestransaction',
            name='items',
            field=models.ManyToManyField(related_name='sales_transactions_as_items', to='inventory.inventoryitem'),
        ),
        migrations.CreateModel(
            name='SoldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.inventoryitem')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_items', to='inventory.salestransaction')),
            ],
        ),
    ]