# Generated by Django 4.2.3 on 2023-10-20 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0008_alter_order_receipt_productimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'order', 'verbose_name_plural': 'orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['created_at', 'price', 'name'], 'verbose_name': 'product', 'verbose_name_plural': 'products'},
        ),
    ]
