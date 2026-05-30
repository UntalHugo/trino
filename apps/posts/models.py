from django.db import models
from django.conf import settings
import re


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.name}'


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField(max_length=280)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.hashtags.clear()
        tags = re.findall(r'#(\w+)', self.content)
        for tag in tags:
            hashtag, _ = Hashtag.objects.get_or_create(name=tag.lower())
            self.hashtags.add(hashtag)

    def __str__(self):
        return f"{self.user.username} - {self.content[:50]}"