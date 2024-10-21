from itertools import chain
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from .models import Post, CategoryParent, Category, Tag, Comment
from .helpers import send_contact

def index(request):
    feature_posts = Post.objects.filter(is_public=True)[:4]
    posts = Post.objects.filter(is_public=True)[:4]
    categories_parents = CategoryParent.objects.all()[:3]
    categories = list(chain(*[c.category_set.all() for c in categories_parents]))
    postsInCategories = list(chain(*[c.post_set.all() for c in categories]))
    latest_posts = Post.objects.filter(is_public=True).order_by('-created_at')[:6]

    popular_posts = Post.objects.filter(is_public=True).order_by('-views')[:4]
    context = {
        'feature_posts': feature_posts,
        'posts': posts,
        'postsInCategories': [post for post in postsInCategories if post.is_public],
        'popular_posts': popular_posts,
        'categories_parents': categories_parents,
        'categories': categories,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/index.html', context=context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id, is_public=True)

    if post is None:
        raise Http404("Post does not exist")
    post.views += 1
    post.save()
    popular_posts = Post.objects.filter(is_public=True).order_by('-views')[:4]
    context = {
        'post': post,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog/blog-detail-01.html', context=context)


def category_parent_detail(request, category_parent_id):
    category_parent = CategoryParent.objects.get(id=category_parent_id)
    if category_parent is None:
        raise Http404("Category does not exist")

    posts = list(chain(*[c.post_set.all() for c in category_parent.category_set.all()]))
    posts = [post for post in posts if post.is_public]
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    page_obj = paginator.page(page_number)
    context = {
        'category': category_parent,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category-01.html', context=context)


def category_detail(request, category_id):
    category = Category.objects.get(id=category_id)
    if category is None:
        raise Http404("Category does not exist")

    posts = category.post_set.filter(is_public=True).order_by('-created_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    page_obj = paginator.page(page_number)
    context = {
        'category': category,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category-01.html', context=context)


def tag_detail(request, tag_id):
    tag = Tag.objects.get(id=tag_id)
    if tag is None:
        raise Http404("Tag does not exist")

    posts = tag.posts.filter(is_public=True).order_by('-created_at')
    page_number = request.GET.get('page', 1)
    paginator = Paginator(posts, 6)
    page_obj = paginator.page(page_number)
    context = {
        'tag': tag,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag.html', context=context)

def search(request):
    query = request.GET.get('q')
    page_number = request.GET.get('page', 1)
    posts = Post.objects.filter(title__icontains=query, is_public=True).order_by('-created_at')
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
                'image': comment.user.customer.image.url,
                'content': comment.content,
                'comment_id': comment.id,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

    return JsonResponse({'success': False})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment is None:
        raise Http404("Comment does not exist")
    comment.delete()
    return redirect('post_detail', post_id=comment.post.id)


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

