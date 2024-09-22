from blog.models import CategoryParent


def categories_parents(request):
    categories = CategoryParent.objects.all()
    return {'categories_parents': categories}