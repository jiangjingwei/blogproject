from django import template
from blog.models import Article, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    """ 最新文章 """
    return Article.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    """ 日期归档 """
    ret = Article.objects.dates('create_time', 'month', order='DESC')
    print(ret)
    return Article.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    """ 分类 """
    return Category.objects.annotate(cate_article_nums=Count('article')).filter(cate_article_nums__gt=0)


@register.simple_tag
def get_tags():
    """ 标签 """
    return Tag.objects.annotate(tag_article_nums=Count('article')).filter(tag_article_nums__gt=0)
