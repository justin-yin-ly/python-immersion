from django.db import models

genre_choices = {
    ('classic','Classic'),
    ('romantic','Romantic'),
    ('comic','Comic'),
    ('fantasy','Fantasy'),
    ('horror','Horror'),
    ('educational','Educational'),
}

book_type_choices = {
    ('hardcover','Hard Cover'),
    ('ebook','E-Book'),
    ('audiobook','Audiobook'),
}

# Create your models here.
class Book(models.Model):
    name=models.CharField(max_length=120)
    author_name=models.CharField(max_length=120,default='unknown')
    price=models.FloatField(help_text='in US Dollars $')
    genre=models.CharField(max_length=12,choices=genre_choices,default='cl')
    book_type=models.CharField(max_length=12,choices=book_type_choices,default='hc')

    def __str__(self):
        return str(self.name)