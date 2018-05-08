from django.shortcuts import render, HttpResponse, get_object_or_404
from blog.models import *
from django.urls import reverse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User


# Create your views here.


# 首页类视图
class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    # 首页分页
    paginate_by = 1


# def index(request):
#
#     # 修改super用户密码
#     # user = User.objects.filter(username='admin').first()
#     # user.set_password('admin')
#     # user.save()
#
#     # article_list = Article.objects.all().order_by('-create_time')
#     article_list = Article.objects.all()
#     return render(request, 'blog/index.html', context={'article_list': article_list})


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/single.html'
    context_object_name = 'article'


    def get(self, request, *args, **kwargs):
        """ 覆写目的将阅读量+1"""
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        # 阅读量+1
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        print('渲染内容')
        """ 覆写的目的将对文章的内容进行markdown渲染"""
        article = super(ArticleDetailView, self).get_object(queryset=None)
        article.content = markdown.markdown(
            article.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )

        return article

    def get_context_data(self, **kwargs):
        print('渲染表单')
        """ 覆写的目的是将article对象和评论表单和评论列表传递给模板 """
        content = super(ArticleDetailView, self).get_context_data(**kwargs)

        form = CommentForm()
        comment_list = self.object.comments_set.all()

        content.update({
            'form': form,
            'comment_list': comment_list
        })

        return content


# def detail(request, pk):
#     # path = reverse("blog:detail", kwargs={'pk': pk})
#     # print(path)
#
#     article = get_object_or_404(Article, pk=pk)
#
#     # 阅读量+1
#     article.increase_views()
#     article.content = markdown.markdown(article.content,
#                                         extensions=[
#                                             'markdown.extensions.extra',
#                                             'markdown.extensions.codehilite',
#                                             'markdown.extensions.toc'
#                                         ])
#
#     form = CommentForm()
#     # 获取全部评论
#     comment_list = article.comments_set.all()
#
#     context = {
#         'article': article,
#         'form': form,
#         'comment_list': comment_list,
#     }
#     return render(request, 'blog/single.html', context=context)


# def archives(request, year, month):
#     # article_list = Article.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
#     article_list = Article.objects.filter(create_time__year=year, create_time__month=month)
#     return render(request, 'blog/index.html', context={'article_list': article_list})

class ArchivesView(IndexView):

    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(create_time__year=self.kwargs.get('year'),
                                                               create_time__month=self.kwargs.get('month'))


# def category(request, pk):
#
#     cate = get_object_or_404(Category, pk=pk)
#     # article_list = Article.objects.filter(category=cate).order_by('-create_time')
#     article_list = Article.objects.filter(category=cate)
#     return render(request, 'blog/index.html', context={'article_list': article_list})

# 分类 类视图
# class CategoryView(ListView):
class CategoryView(IndexView):
    # model = 'Category'
    # template_name = 'blog/index.html'
    # context_object_name = 'article_list'

    def get_queryset(self):
        print('args++++++++', self.args)
        print('kwargs++++++++', self.kwargs)
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
