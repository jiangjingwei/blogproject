from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):

    """ 文章分类 """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):

    """ 文章标签 """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):

    """ 文章"""

    title = models.CharField(max_length=70)

    content = models.TextField()

    # 文章创建时间
    create_time = models.DateTimeField()

    # 最后一次文章修改时间
    update_time = models.DateTimeField()

    # 文章摘要，可以为空白
    summary = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)

    tags = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User)

    def __str__(self):
        return self.title
