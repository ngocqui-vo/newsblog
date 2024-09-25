from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('category-parent/<int:category_parent_id>', views.category_parent_detail, name='category_parent_detail'),
]
