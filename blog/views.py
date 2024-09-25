from itertools import chain

from django.http import Http404
from django.shortcuts import render
from .models import Post, CategoryParent, Category

def index(request):
    feature_posts = Post.objects.all()[:4]
    posts = Post.objects.all()[:4]
    categories_parents = CategoryParent.objects.all()[:3]
    categories = list(chain(*[c.category_set.all() for c in categories_parents]))
    postsInCategories = list(chain(*[c.post_set.all() for c in categories]))
    latest_posts = Post.objects.all().order_by('-created_at')[:6]

    popular_posts = Post.objects.all().order_by('-views')[:4]
    context = {
        'feature_posts': feature_posts,
        'posts': posts,
        'postsInCategories': postsInCategories,
        'popular_posts': popular_posts,
        'categories_parents': categories_parents,
        'categories': categories,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/index.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.views += 1
    post.save()
    popular_posts = Post.objects.all().order_by('-views')[:4]
    if post is None:
        raise Http404("Post does not exist")
    context = {
        'post': post,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/blog-detail-01.html', context=context)


def get_categories(request, category_parent_id):
    categories = Category.objects.filter(parent_id=category_parent_id)
    if categories is None:
        raise Http404("Category does not exist")
    return render(request, 'blog/category-01.html', context= {'categories': categories})


def category_parent_detail(request, category_parent_id):
    category_parent = CategoryParent.objects.get(id=category_parent_id)
    if category_parent is None:
        raise Http404("Category does not exist")
    return render(request, 'blog/category-01.html', context= {'category_parent': category_parent})