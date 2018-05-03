from django import template
from blog.models import Article, Category

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    """ 最新文章模板标签 """
    return Article.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    """ 归档模板标签 """
    ret = Article.objects.dates('create_time', 'month', order='DESC')
    print(ret)
    return Article.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """ 分类模板标签 """
    return Category.objects.all()