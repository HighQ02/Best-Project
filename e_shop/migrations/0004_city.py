# Generated by Django 4.2.3 on 2023-08-07 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop', '0003_category_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=168)),
            ],
            options={
                'verbose_name': 'Города',
                'verbose_name_plural': 'Города',
            },
        ),
    ]
