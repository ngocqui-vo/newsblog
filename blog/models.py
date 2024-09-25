from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class CategoryParent(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=300)
    parent = models.ForeignKey(CategoryParent, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return self.title
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = RichTextField()
    image = models.ImageField(upload_to='blog/images/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class Tag(models.Model):
    name = models.CharField(max_length=300)
    posts = models.ManyToManyField(Post, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
