from django.http import Http404
from django.shortcuts import render
from . import models


def index(request):
    feature_posts = models.Post.objects.all()[:4]
    posts = models.Post.objects.all()[:4]
    categories = models.Category.objects.all()[:3]
    popular_posts = models.Post.objects.all().order_by('-views')[:5]
    context = {
        'feature_posts': feature_posts,
        'posts': posts,
        'categories': categories,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/index.html', context=context)


def post_detail(request, post_id):
    post = models.Post.objects.get(pk=post_id)
    if post is None:
        raise Http404("Post does not exist")
    return render(request, 'blog/blog-detail-01.html', context= {'post':post})


def get_categories(request, category_parent_id):
    categories = models.Category.objects.filter(parent_id=category_parent_id)
    if categories is None:
        raise Http404("Category does not exist")
    return render(request, 'blog/category-01.html', context= {'categories': categories})


