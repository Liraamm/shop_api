# Generated by Django 4.1.5 on 2023-01-23 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_logic', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Артикул', 'verbose_name_plural': 'Артикли'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Продукт', 'verbose_name_plural': 'Продукты'},
        ),
    ]
