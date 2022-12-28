from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager




# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username,  password=None):
        if not username:
            raise ValueError("User must have an username")
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            username=self.normalize_username(username),
            email=self.normalize_email(email)
        )
        user.set_password(password)  # change password to hash
        user.save()
        return user
        
    def create_superuser(self, username,  password=None, **extra_fields):
        if not username:
            raise ValueError("User must have an username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            username=self.normalize_username(username)
        )
        user.set_password(password)
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractUser):
    fullname = models.CharField("Full Name", max_length=100,  null=True, blank=True)
    address = models.TextField("Address", null=True, blank=True)
    phone = models.CharField("Phone Number", max_length=15, null=True, blank=True)
    avatar = models.ImageField("Profile Picture", upload_to="avatar/", default="avatar/man.png")
    is_verified = models.BooleanField(default=False)
        # this part makes the user user to login using username instead of username
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


    
    