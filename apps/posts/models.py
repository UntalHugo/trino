from django.db import models
from django.conf import settings
import re

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    mentions = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='mentioned_in'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"

    def extract_hashtags(self):
        return re.findall(r'#(\w+)', self.content)

    def extract_mentions(self):
        return re.findall(r'@(\w+)', self.content)