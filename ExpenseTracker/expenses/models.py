from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
#Create your models here.

CHOICES =[
    ("Student","Student"),
    ("Employee","Employee"),
    ("Other","Other")
]

class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'category'
        ordering = ['name'] 
        
    def __str__(self):
        return self.name
    
class Expense(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,default="null") 
    quantity = models.BigIntegerField()
    Date = models.DateField(default = now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Budget(models.Model):
    user = models.ForeignKey(User,default = 1, on_delete=models.CASCADE)
    budget_limit = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

        
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profession = models.CharField(max_length = 10, choices=CHOICES, default="null")
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    def __str__(self):
       return self.user.username
   

