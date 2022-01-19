from typing import AbstractSet
from django.db import models
from django.http import request
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager



# Create your models here.

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self,email,user_name,first_name,last_name,password,**other_fields) :
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)
        other_fields.setdefault('is_active',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        return self.create_user(email,user_name,first_name,last_name,password,**other_fields)

    def create_user(self,email,user_name,first_name,last_name,password,gender,birthday,**other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email,user_name=user_name,first_name=first_name,last_name=last_name,gender=gender,birthday=birthday,**other_fields)
        user.set_password(password)
        user.save()
        return user

class User(AbstractUser,PermissionsMixin):
    email=models.EmailField(unique=True)
    user_name=models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    is_staff= models.BooleanField(default=False)
    is_active= models.BooleanField(default=False)
    birthday=models.DateField(null=False)
    gender = models.CharField(max_length=1,null=False) 
    userImage=models.ImageField(upload_to="users",null=True)
    objects = CustomAccountManager()

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ["user_name","first_name","last_name","gender","birthday"]

    def __str__(self):
        return self.user_name
    
