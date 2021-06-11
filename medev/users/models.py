from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from autoslug import AutoSlugField

from .managers import MyUserManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=16, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    description = models.CharField(max_length=150, blank=True, null=True)

    slug = AutoSlugField(
        null=True,
        default=None,
        unique=True,
        populate_from='username',
        always_update=True
    )

    """
    profile_picture = models.ImageField(
        upload_to='uploads/avatars',
        default='uploads/avatars/default_avatar.png'
    )
    """

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
