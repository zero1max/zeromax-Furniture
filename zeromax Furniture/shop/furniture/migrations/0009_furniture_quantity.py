# Generated by Django 5.0.6 on 2024-06-23 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('furniture', '0008_customer_order_orderproduct_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='furniture',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Product Quantity'),
        ),
    ]
