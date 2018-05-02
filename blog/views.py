from django.shortcuts import render, HttpResponse
from blog.models import *
# Create your views here.


def index(request):

    article_list = Article.objects.all().order_by('-create_time')

    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的首页',
        'article_list': article_list,
    })
