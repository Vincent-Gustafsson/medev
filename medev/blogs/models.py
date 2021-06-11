from django.db import models

from core.models import BaseModel


class Post(BaseModel):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    thumbnail = models.ImageField(upload_to='blogs/posts/thumbnail')

    author = models.ForeignKey(
        'User',
        related_name='posts',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title