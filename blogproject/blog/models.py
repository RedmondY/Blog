from django.db import models

# Create your models here.
import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

class Category(models.Model):
    '''
    定义文章种类的名字
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    '''
    定义标签
    '''
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    '''
    文章的定义
    '''

    # 标题
    title = models.CharField('标题', max_length=70)

    # 正文
    body = models.TextField('正文')

    # toc = models.CharField('目录',max_length=200, blank=True)

    # 创建以及修改时间
    created_time = models.DateTimeField('创建时间', default=timezone.now) # now()?now?
    modified_time = models.DateTimeField('修改时间')

    # 文章摘要
    excerpt = models.CharField('摘要',max_length=200, blank=True)

    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)

    # 作者
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time', 'title']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:50]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    # revesrse 会解析这个视图函数对应的URL
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
