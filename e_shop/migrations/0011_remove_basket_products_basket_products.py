# Generated by Django 4.2.3 on 2023-08-24 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0010_remove_basket_quantity_alter_basket_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='products',
        ),
        migrations.AddField(
            model_name='basket',
            name='products',
            field=models.ManyToManyField(to='e_shop.boughtproducts'),
        ),
    ]