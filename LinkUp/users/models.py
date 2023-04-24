from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

GENDER_CHOICES = {
    ('Male','Male'),
    ('Female','Female'),
    ('Transgenders','Transgenders')
}


class UserManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        if not username:
            raise ValueError('The Username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, username, **extra_fields)


class user(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    username = models.CharField(max_length=250,unique=True)
    full_name = models.CharField(max_length=250,blank=True)
    profile = models.ImageField(upload_to='profile',blank=True)
    gender = models.CharField(max_length=25,choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15,unique=True)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField()
    followers = models.IntegerField()
    following = models.IntegerField()
    password = models.CharField(max_length=25)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email