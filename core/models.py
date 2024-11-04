"""
Database models.
"""
import uuid
import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager

def recipe_image_file_path(instance,filename):
     """Generate file path for new recipe image"""
     ext=os.path.splitext(filename)[1]
     filename=f'{uuid.uuid4()}{ext}'

     return os.path.join('uploads','recipe',filename)

class CustomUserManager(BaseUserManager):

     def create_user(self,email,name,password=None,**extra_fields):
          if not email:
               raise ValueError('The Email field must be set')
          email=self.normalize_email(email)
          user=self.model(email=email,name=name, **extra_fields)
          user.set_password(password)
          user.save(using=self._db)

          return user

     def create_superuser(self,email,password=None,**extra_fields):
          extra_fields.setdefault('is_staff',True)
          extra_fields.setdefault('is_superuser',True)

          if extra_fields.get('is_staff') is not True:
               raise ValueError('Superuser must have is_staff=True')
          if extra_fields.get('is_superuser') is not True:
               raise ValueError('Superuser must have is_superuser=True.')

          return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=CustomUserManager()

    USERNAME_FIELD='email'

class Recipe(models.Model):
     """Recipe object"""
     user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
     title=models.CharField(max_length=255)
     description=models.TextField(blank=True)
     time_minutes=models.IntegerField()
     price=models.DecimalField(max_digits=5,decimal_places=2)
     link=models.CharField(max_length=255,blank=True)
     tags=models.ManyToManyField('Tag')
     ingredients=models.ManyToManyField('Ingredient')
     image=models.ImageField(null=True,upload_to=recipe_image_file_path)

     def __str__(self):
          return self.title

class Tag(models.Model):
     """Tag fpr filtering recipes"""
     name=models.CharField(max_length=255)
     user=models.ForeignKey(
          settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE
     )

     def __str__(self):
          return self.name

class Ingredient(models.Model):
     name=models.CharField(max_length=255)
     user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

     def __str__(self):
          return self.name