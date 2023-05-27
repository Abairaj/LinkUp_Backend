from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

GENDER_CHOICES = {
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Transgenders', 'Transgenders')
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
    username = models.CharField(max_length=250)
    full_name = models.CharField(max_length=250, blank=True)
    facebook_uid = models.CharField(max_length=500, blank=True)
    profile = models.ImageField(upload_to='profile', blank=True, null=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    about = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)
    followers = models.ManyToManyField('self',symmetrical=False,related_name='followings')
    following = models.ManyToManyField('self',symmetrical=False)
    password = models.CharField(max_length=250)
    is_banned = models.BooleanField(default=False, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email
