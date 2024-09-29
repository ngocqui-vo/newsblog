from itertools import chain
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Post, CategoryParent, Category
from .helpers import send_contact

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
    cate = Category.objects.get(pk=post_id)
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
    category_parent = Category.objects.get(parent_id=category_parent_id)
    if category_parent is None:
        raise Http404("Category does not exist")
    return render(request, 'blog/category-01.html', context= {'category_parent': category_parent})


def category_parent_detail(request, category_parent_id):
    category_parent = CategoryParent.objects.get(id=category_parent_id)
    if category_parent is None:
        raise Http404("Category does not exist")

    posts = list(chain(*[c.post_set.all() for c in category_parent.category_set.all()]))
    context = {
        'category_parent': category_parent,
        'posts': posts,
    }
    return render(request, 'blog/category-01.html', context=context)


def search(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page', 1)
    posts = Post.objects.filter(title__icontains=query).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_obj = paginator.page(page_number)
    context = {
        'paginator': paginator,
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'blog/blog-list-01.html', context=context)


def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return JsonResponse({
                'success': True,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

    return JsonResponse({'success': False})


def contact_us(request):
    if request.method == 'GET':
        return render(request, 'blog/contact.html', context={})
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        website = request.POST.get('website', '')
        message = request.POST.get('message', '')
        send_contact('dzlama101@gmail.com',name, email, website, message)
        return JsonResponse({'success': True})


def about(request):
    return render(request, 'blog/about.html', context={})

