# Generated by Django 4.1.5 on 2023-01-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_logic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_at',
            field=models.DateField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]