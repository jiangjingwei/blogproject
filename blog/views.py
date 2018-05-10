from django.shortcuts import render, HttpResponse, get_object_or_404
from blog.models import *
from django.urls import reverse
import markdown
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q


# Create your views here.


# 首页类视图
class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    # 首页分页
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page_obj = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator, page_obj, is_paginated)

        context.update(pagination_data)

        return context

    def pagination_data(self, paginator, page_obj, is_paginated):

        # 如果没有分页
        if not is_paginated:
            return {}

        # 当前页左边的号码
        left = []

        # 当前页右边的号码
        right = []

        # 左边是否要有省略号
        left_has_more = False

        # 右边是否要有省略号
        right_has_more = False

        # 是否要显示第一页，如果当前页的左边连续页码中包含第一页就不需要显示第一页页码
        first = False

        # 是否要显示最后一页，如果当前页的左边连续页码中包含最后一页就不需要显示最后一页页码
        last = False

        # 用户当前页码
        current_page_num = page_obj.number

        # 用户总页数
        total_pages = paginator.num_pages

        # 整个分页的页码列表
        page_num_list = paginator.page_range

        # 判断当前页是否是第一页
        if current_page_num == 1:

            # 右边显示的页码
            right = page_num_list[current_page_num:current_page_num + 2]

            if right[-1] < total_pages - 1:
                # 右边是否显示省略号
                right_has_more = True

            if right[-1] < total_pages:
                # 是否显示最后一页
                last = True

        # 判断当前页是否是最后一页
        elif current_page_num == total_pages:
            left = page_num_list[(current_page_num - 3) if (current_page_num - 3) > 0 else 0:current_page_num - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:

            right = page_num_list[current_page_num:current_page_num + 2]
            left = page_num_list[(current_page_num - 3) if (current_page_num - 3) > 0 else 0:current_page_num - 1]

            # 是否显示最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 是否显示最后一页
            if right[-1] < total_pages:
                last = True

            # 是否显示第一页后面的省略号
            if left[0] > 2:
                left_has_more = True

            # 是否显示第一页
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last
        }

        return data


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
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            # 'markdown.extensions.toc',
            # 美化文章目录在url中的锚点
            TocExtension(slugify=slugify)
        ])

        article.content = md.convert(article.content)
        article.toc = md.toc

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


class TagView(IndexView):

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


def search(request):
    """ 全文检索 """
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    article_list = Article.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))

    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'article_list': article_list
                                               })

