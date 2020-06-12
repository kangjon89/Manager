from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords must match"
        return errors

    def login_validator(self, postData):
        errors = {}
        try: 
            existing = User.objects.get(email=postData['email'])
        except:
            errors['login_email'] = "Please make sure you're using a valid email or password"
            return errors
        if not bcrypt.checkpw(postData['password'].encode(), existing.password.encode()):
            errors['login_password'] = "Please make sure you're using a valid email or password"
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
