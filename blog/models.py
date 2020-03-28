from django.db import models
from django.contrib import  admin
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    created_time = models.CharField(max_length=50, default=now)
    comment_num = models.PositiveIntegerField(verbose_name='评论数', default=0)

    def __str__(self):
        return self.username

    def comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

    def comment_del(self):
        self.comment_num -= 1
        self.save(update_fields=['comment_num'])
    class Meta:  # 按时间下降排序
        ordering = ['-created_time']
        verbose_name = '用户'  # 指定后台显示模型名称
        verbose_name_plural = '用户列表'  # 指定后台显示模型复数名称
        db_table = "user"  # 数据库表名


class Article(models.Model):
    title = models.CharField(max_length=100)  # 博客题目
    category = models.TextField(max_length=50, blank=True)  # 博客标签
    date_time = models.DateTimeField(auto_now_add=True)  # 博客日期
    content = models.TextField(blank=True, null=True)  # 博客文章正文

    def __unicode__(self):
        return self.title

    class Meta:  # 按时间下降排序
        ordering = ['-date_time']
        verbose_name = '博客'  # 指定后台显示模型名称
        verbose_name_plural = '博客列表'  # 指定后台显示模型复数名称
        db_table = "blog"  # 数据库表名

class ArticleComment(models.Model):
    body = models.TextField()
    username = models.CharField(max_length=50)
    date_time = models.DateTimeField(verbose_name='创建时间', default=now)
    article = models.CharField(max_length=50)
    # 使对象在后台显示更友好
    def __str__(self):
        return self.article

    class Meta:
        ordering = ['-date_time']
        verbose_name = '评论'  # 指定后台显示模型名称
        verbose_name_plural = '评论列表'  # 指定后台显示模型复数名称
        db_table = "comment"  # 数据库表名

    list_display = ('article', 'body')



