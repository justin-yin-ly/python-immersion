from django.db import models
from books.models import Book

# Create your models here.
class Sale(models.Model):
    book=models.ForeignKey(Book,on_delete=models.CASCADE,default=None)
    quantity=models.PositiveIntegerField()
    price=models.FloatField(help_text='in US Dollars $')
    date_created=models.DateTimeField()

    def __str__(self):
        return f"id: {self.id}, book: {self.book.name}, quantity: {self.quantity}"