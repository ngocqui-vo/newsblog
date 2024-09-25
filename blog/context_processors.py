from blog.models import CategoryParent, Tag, Post


def categories_parents(request):
    categories = CategoryParent.objects.all()
    return {'categories_parents': categories}


def get_tags(request):
    tags = Tag.objects.all()
    return {'tags': tags}


def get_popular_posts(request):
    popular_posts = Post.objects.all().order_by('-views')[:4]
    return {'popular_posts': popular_posts}