from django.contrib import admin

from blog.models import Category, Post, Tag, Comment, CategoryParent

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryParent)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)

