from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self):
        return "{}".format(self.email)


class AuthorPost(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    body = models.TextField(max_length=256, blank=True, null=True)
    author = models.ForeignKey(User, related_name='author_post', null=True, blank=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)


class BlockAuthor(models.Model):
    block_by = models.ForeignKey(User, related_name='block_by', null=True, blank=True, on_delete=models.CASCADE)
    blocked_to = models.ForeignKey(User, related_name='blocked_to', null=True, blank=True, on_delete=models.CASCADE)

