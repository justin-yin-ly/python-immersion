# Generated by Django 4.2.14 on 2024-07-18 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_sale_book_alter_sale_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date_created',
            field=models.DateField(),
        ),
    ]
