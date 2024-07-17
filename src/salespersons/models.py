from django.db import models

# Create your models here.
class Salesperson(models.Model):
    username=models.CharField(max_length=120)
    name=models.CharField(max_length=120)
    pic = models.ImageField(upload_to='salespersons',default='no_picture.jpg')
    bio=models.TextField()

    def __str__(self):
        return str(self.username)