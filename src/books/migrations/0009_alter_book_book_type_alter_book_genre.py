# Generated by Django 4.2.14 on 2024-07-18 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_alter_book_book_type_alter_book_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_type',
            field=models.CharField(choices=[('hardcover', 'Hard Cover'), ('ebook', 'E-Book'), ('audiobook', 'Audiobook')], default='hc', max_length=12),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('romantic', 'Romantic'), ('horror', 'Horror'), ('comic', 'Comic'), ('classic', 'Classic'), ('fantasy', 'Fantasy'), ('educational', 'Educational')], default='cl', max_length=12),
        ),
    ]
