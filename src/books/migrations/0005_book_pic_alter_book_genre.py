# Generated by Django 4.2.14 on 2024-07-16 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_book_type_alter_book_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pic',
            field=models.ImageField(default='no_picture.jpg', upload_to='books'),
        ),
        migrations.AlterField(
            model_name='book',
            name='genre',
            field=models.CharField(choices=[('comic', 'Comic'), ('horror', 'Horror'), ('educational', 'Educational'), ('classic', 'Classic'), ('romantic', 'Romantic'), ('fantasy', 'Fantasy')], default='cl', max_length=12),
        ),
    ]