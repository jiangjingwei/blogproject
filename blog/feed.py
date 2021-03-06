from django.contrib.syndication.views import Feed
from blog.models import Article


class AllArticleRssFeed(Feed):

    # 显示在聚合阅读器上的标题
    title = "Django 博客教程演示项目"

    # 通过聚合阅读器跳转到网站的地址
    link = "/"

    # 现在在聚合阅读器上的描述信息
    description = "Django 博客教程演示项目测试文章"

    # 显示的内容条目
    def items(self):
        return Article.objects.all()

    # 聚合器显示的内容条目的标题
    def item_title(self, item):
        return "【%s】  %s" % (item.category, item.title)

    # 聚合器显示的内容条目的描述
    def item_description(self, item):
        return item.content

