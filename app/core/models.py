from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email instead of usernames
    """
    email = models.EmailField(max_length=500, unique=True)
    name = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # assign username field to email
    USERNAME_FIELD = 'email'
