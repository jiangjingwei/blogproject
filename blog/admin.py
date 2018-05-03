from django.contrib import admin
from blog.models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):

    list_display = ['title', 'create_time', 'update_time', 'category', 'author']


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
