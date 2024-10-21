from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>', views.post_detail, name='post_detail'),
    path('category-parent/<int:category_parent_id>', views.category_parent_detail, name='category_parent_detail'),
    path('category/<int:category_id>', views.category_detail, name='category_detail'),
    path('tag/<int:tag_id>', views.tag_detail, name='tag_detail'),
    path('contact-us', views.contact_us, name='contact_us'),
    path('about', views.about, name='about'),
]
