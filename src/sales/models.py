from django.db import models

# Create your models here.
class Sale(models.Model):
    # book = | Variable that holds reference to the book that was sold
    quantity=models.IntegerField()
    price=models.FloatField(help_text='in US Dollars $')
    date_created=models.DateField()