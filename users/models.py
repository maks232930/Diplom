from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('У пользователя должен быть email')
        if not username:
            raise ValueError('Должнен быть username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, first_name=None, last_name=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name

        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField('Имя', max_length=50, null=True)
    last_name = models.CharField('Фамилия', max_length=50, null=True)
    is_blocked = models.BooleanField(default=False, verbose_name='Заблокировать')
    is_active = models.BooleanField(default=True, verbose_name='Доступ в админку')

    objects = UserManager()  # example Model.objects

    USERNAME_FIELD = 'email'  # authorization field
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # additional fields for createsuperuser

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        if self.is_blocked is True:
            if self.is_superuser is True:
                return True
            return False
        return self.is_superuser or self.is_active

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
