# Generated by Django 4.2.7 on 2023-11-29 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_category_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.FileField(default='Нет фото', upload_to='categories/', verbose_name='Изображение категорий'),
        ),
    ]