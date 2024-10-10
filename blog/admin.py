from django.contrib import admin

from blog.models import Category, Post, Tag, Comment, CategoryParent


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_category_title', 'created_at')
    list_display_links = ('id',)
    search_fields = ('title', 'category__title')
    ordering = ('title', 'created_at')
    list_editable = ('title',)

    def get_category_title(self, obj):
        return obj.category.title
    get_category_title.short_description = 'Category'


# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryParent)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)

