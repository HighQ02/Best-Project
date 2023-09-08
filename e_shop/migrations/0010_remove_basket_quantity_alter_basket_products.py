# Generated by Django 4.2.3 on 2023-08-24 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0009_rename_product_basket_products_boughtproducts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='basket',
            name='products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='e_shop.boughtproducts'),
        ),
    ]