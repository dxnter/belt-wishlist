from __future__ import unicode_literals
import re
import bcrypt, datetime
from dateutil.parser import parse as parse_date
from django.db import models


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['registration_name']) < 3:
            errors['registration_name'] = "Name cannot be shorter than 3 characters"

        if len(postData['registration_username']) < 3:
            errors['registration_username'] = "Username cannot be shorter than 3 characters"

        if (User.objects.filter(username=postData['registration_username']).exists()):
            errors['registration_user_exists'] = "A user with that username already exists"

        if len(postData['registration_password']) < 8:
            errors['registration_password'] = "Password is too short"

        if postData['registration_password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match"
            
        if len(postData['date_hired']) == 0:
            errors['date_hired'] = "Please enter a date"
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if (User.objects.filter(username=postData['login_username']).exists()) == False:
            errors['login_false'] = "A user with that username does not exist"

        if (User.objects.filter(username=postData['login_username']).exists()):
            user = User.objects.filter(username=postData['login_username'])[0]
            if (bcrypt.checkpw(postData['login_password'].encode(), user.password.encode())) == False:
                errors['wrong_password'] = "Incorrect password"

        if len(postData['login_username']) == 0:
            errors['login_username'] = "You must enter a username"

        if len(postData['login_password']) == 0:
            errors['login_password'] = "You must enter a password"

        return errors

    def item_validator(self, postData):
        errors = {}
        if len(postData['item']) == 0:
            errors['item_empty'] = "You must enter an item"

        if len(postData['item']) < 3:
            errors['short_item'] = "Item name must be more than 3 characters"   
        return errors
    


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateTimeField()
    items = models.ManyToManyField('Item')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()