# Generated by Django 4.1.4 on 2023-01-01 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='zipcode',
            new_name='tel',
        ),
    ]
