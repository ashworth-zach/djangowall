from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        user=User.objects.all().values().filter(email=postData['email'])
        if user:
            errors["user"] = "email already exists in database"
        if len(postData['firstname']) < 2:
            errors["firstname"] = "firstname cannot be less than 2 characters"
        if postData['firstname'].isalpha() is False:
            errors["firstname"] = "first name cannot contain numbers"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "last name must be longer than 2 characters"
        if postData['lastname'].isalpha() is False:
            errors["lastname"] = "last name cannot contain numbers"
        if len(postData['password']) < 8 :
            errors["password"] = "password cannot be less than 8 characters"
        if postData['password'] != postData['passwordconf'] :
            errors["passwordconf"] = "passwords do not match"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "email is invalid"            
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData['password']) < 1 :
            errors["password"] = "please enter your password"
        try:
            user=User.objects.all().values().get(email=postData['email'])
            if user:
                if bcrypt.checkpw(postData['password'].encode(), user['pwhash'].encode()):
                    print("password match")
                else:
                    errors["password"] = "passwords do not match"
                return errors
        except:
            errors['login']="user does not exist in database"
            return errors
class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    pwhash = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # *************************
    # Connect an instance of UserManager to our User model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    objects = UserManager()
    # *************************
class Message(models.Model):
    user=models.ForeignKey(User, related_name="messages")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Comment(models.Model):
    message = models.ForeignKey(Message, related_name="comments")
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

