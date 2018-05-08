from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown
from django.utils.html import strip_tags

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


@python_2_unicode_compatible
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

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        """ 文章摘要自动根据文章保存 """
        if not self.summary:
            md = markdown.markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            self.summary = strip_tags(md.convert(self.content))[:54]

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-create_time']
