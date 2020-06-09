from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    LANGUAGE_TYPES = (
        ('EN', 'English'),
        ('JP', 'Japanese'),
        ('FR', 'French'),
        ('SP', 'Spanish'),
        ('PT', 'Portguese'),
        ('CN', 'Chinese'),
        ('KR', 'Korean'),
        ('DE', 'German'),
    )
    title = models.TextField(max_length=150)
    embed_link = models.URLField(default=None, max_length=300)
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    #slug = models.SlugField(unique=True, max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #tags = TaggableManager()
    
    def __str__(self):
        return self.content[:5]

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()
    
    @property
    def number_of_favorites(self):
         return Favorite.objects.filter(post_connected=self).count()
    
class Favorite(models.Model):
    favoriter = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)
