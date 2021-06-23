from django.db import models
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField

from core.models import BaseModel


User = get_user_model()


class Post(BaseModel):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)

    slug = AutoSlugField(
        null=True,
        default=None,
        unique=True,
        populate_from='title',
        always_update=True
    )

    author = models.ForeignKey(
        User,
        related_name='posts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title