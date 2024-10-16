from blog.models import CategoryParent, Tag, Post, Category


def categories_parents(request):
    categories = CategoryParent.objects.all()
    return {'cat_parents': categories}


def get_tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}


def get_popular_posts(request):
    popular_posts = Post.objects.all().order_by('-views')[:4]
    return {'popular_posts': popular_posts}


def get_categories(request):
    categories = Category.objects.all()[:5]
    return {'categories': categories}