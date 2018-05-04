from django.shortcuts import render, HttpResponse, get_object_or_404
from blog.models import *
from django.urls import reverse
import markdown
from comments.forms import CommentForm

from django.contrib.auth.models import User
# Create your views here.


def index(request):

    # 修改super用户密码
    # user = User.objects.filter(username='admin').first()
    # user.set_password('admin')
    # user.save()

    # article_list = Article.objects.all().order_by('-create_time')
    article_list = Article.objects.all()
    return render(request, 'blog/index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的首页',
        'article_list': article_list,
    })


def detail(request, pk):

    # path = reverse("blog:detail", kwargs={'pk': pk})
    # print(path)

    article = get_object_or_404(Article, pk=pk)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                            'markdown.extensions.toc'
                                        ])

    form = CommentForm()
    # 获取全部评论
    comment_list = article.comments_set.all()

    context = {
        'article': article,
        'form': form,
        'comment_list': comment_list,
    }

    return render(request, 'blog/single.html', context=context)


def archives(request, year, month):
    # article_list = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    article_list = Article.objects.filter(create_time__year=year, create_time__month=month)
    return render(request, 'blog/index.html', context={'article_list': article_list})


def category(request, pk):

    cate = get_object_or_404(Category, pk=pk)
    # article_list = Article.objects.filter(category=cate).order_by('-create_time')
    article_list = Article.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'article_list': article_list})

