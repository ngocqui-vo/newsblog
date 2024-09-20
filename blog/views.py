from django.shortcuts import render
from . import models
# Create your views here.

import random
def index(request):
    posts = models.Post.objects.all()[0]


    return render(request, 'blog/index.html', context= {'post':post})
