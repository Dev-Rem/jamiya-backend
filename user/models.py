from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from jamiyafx.models.variables import *
from datetime import datetime

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, first_name, last_name, password, station=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not first_name:
            raise ValueError('The first name field must be set')
        if not last_name:
            raise ValueError('The last name field must be set')
        if not email:
            raise ValueError("The email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.station = station
        user.set_password(password)
        
        user.save()
        return user

    def create_superuser(self,  email,username, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email,username, first_name, last_name, password, **extra_fields)
    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    station = models.CharField(max_length=50, choices=EMPLOYEE_STATIONS, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    
    date_joined = models.DateField(
        verbose_name="Date Joined", auto_now=False, default=datetime.now
    )
    last_login = models.DateTimeField(
        verbose_name="Date Last log in", default=datetime.now)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',"first_name", 'last_name']

    def __str__(self):
        return self.email
    

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin
