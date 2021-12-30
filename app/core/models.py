from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

from django.conf import settings


class UserManager(BaseUserManager):
    """
    Provides helper functions to create user
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save new user
        """
        if not email:
            raise ValueError
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        return self.save_and_return(user)

    def create_superuser(self, email, password):
        """
        Creates superuser
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        return self.save_and_return(user)

    def save_and_return(self, user):
        """
        common save and return utility
        """
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of usernames
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # assign username field to email
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """
    Tag to be used in recipe
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
