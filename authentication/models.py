from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    """
    This module allows to define custom manager. Thus you can customize your User DB
    """

    def create_user(self, *, username, password, **kwargs):
        if not username:
            raise ValueError('username is required')
        if not password:
            raise ValueError('password is required')

        user = self.model(
            username=self.normalize_email(username),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def get_by_natural_key(self, username):
        """
        This method is called every time when a request is arrived.
        """
        user = self.get(**{self.model.USERNAME_FIELD: username})
        return user


class User(AbstractBaseUser):
    class UserType(models.IntegerChoices):
        ADMIN = 1
        USER = 2
        RESTAURANT = 3

    username = models.CharField(max_length=200, unique=True, null=True)
    first_name = models.CharField(max_length=128, null=True)
    last_name = models.CharField(max_length=128, null=True)
    user_type = models.IntegerField(null=True, choices=UserType.choices, default=UserType.USER)
    USERNAME_FIELD = 'username'
    objects = UserManager()
    is_login = models.BooleanField(default=False)  # To check if user can order
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.password and self.username and not self.password.startswith('pbkdf2_sha256'):
            # In case of call User.object.create() or User().save()
            self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'db_user'
