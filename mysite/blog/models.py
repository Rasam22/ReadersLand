from django.db import models

# Create your models here.
class signup(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    email=models.EmailField()
    isActive=models.IntegerField(default='2')
    password=models.CharField(max_length=20,default='123456')