from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from bs4 import BeautifulSoup
from django.core.validators import FileExtensionValidator
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
    image = models.ImageField(upload_to='blog/images/', blank=False, null=False, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)

    def __str__(self) -> str:
        draft = 'Draft - ' if not self.is_public else ''
        return f'{draft}{self.title}'

    def get_excerpt(self, length=100):
        soup = BeautifulSoup(self.content, 'html.parser')
        text = soup.get_text()
        return text[:length]


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content}'


class Tag(models.Model):
    name = models.CharField(max_length=300)
    posts = models.ManyToManyField(Post, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
