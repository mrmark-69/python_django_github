# Generated by Django 4.2.3 on 2023-08-13 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0008_alter_product_options_alter_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['created_at', 'price', 'name']},
        ),
    ]