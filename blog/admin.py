from django.contrib import admin
from blog.models import Article,User,ArticleComment

# Register your models here.
admin.site.register(Article)
admin.site.register(User)
admin.site.register(ArticleComment)