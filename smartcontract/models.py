from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    manufacturer  = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='manufacturer') 
    retailer  = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='retailer')
    owner  = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name='owner') 
    name = models.CharField(max_length=50)
    desc = models.TextField()
    # slug = models.SlugField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
