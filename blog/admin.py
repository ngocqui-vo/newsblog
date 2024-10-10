from django.contrib import admin

from blog.models import Category, Post, Tag, Comment, CategoryParent


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_category_title', 'created_at')
    list_display_links = ('id',)
    search_fields = ('title', 'category__title')
    ordering = ('title', 'created_at')
    exclude = ('user',)  # Loại bỏ user khỏi form cho user thường

    def get_category_title(self, obj):
        return obj.category.title
    get_category_title.short_description = 'Category'

    # Chỉ hiển thị các post của chính user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    # Quyền chỉnh sửa post
    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.user == request.user
        return True

    # Quyền xóa post
    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.user == request.user
        return True

    # Chỉ cho phép thêm post nếu user đã đăng nhập
    def has_add_permission(self, request):
        return request.user.is_authenticated

    # Ẩn các model khác đối với user thường
    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {
            'add': True,
            'change': True,
            'delete': True,
        }

    # Chỉnh sửa form: Admin có thể chỉnh sửa `views`, user thường không thể
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['views'].disabled = True  # Vô hiệu hóa trường 'views' cho user thường
        return form

    # Gán user hiện tại cho post khi lưu
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user  # Gán user hiện tại vào post
        super().save_model(request, obj, form, change)

# Register your models here.
admin.site.register(Category)
admin.site.register(CategoryParent)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)

