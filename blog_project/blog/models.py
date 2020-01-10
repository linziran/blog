from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#tag（标签）
class User(AbstractUser):
    avater = models.ImageField(upload_to='avatar/%Y/%m',default='avatar/default.png',max_length=200)
    qq = models.CharField(max_length=20,blank=True,null=True,verbose_name='QQ号码')
    mobile = models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name='手机号码')
    url = models.URLField(max_length=100,blank=True,null=True,verbose_name='个人网页地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering =  ['-id']

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30,verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
#分类
class Catagory(models.Model):
    name = models.CharField(max_length=30,verbose_name='分类名称')
    index = models.IntegerField(default=999,verbose_name='分类的排序')

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

#自定义一个文章Model的管理器
#1、新加一个数据处理的方式
#2、改变原有的queryset
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            date = date['date_publish'].strftime('%Y/%m{a}').format(a='文章存档')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

#文章模型
class Article(models.Model):
    title = models.CharField(max_length=50,verbose_name='文章标题')
    desc = models.CharField(max_length=50,verbose_name='文章描述')
    content = models.TextField(verbose_name="文章内容")
    click_count = models.IntegerField(default=0,verbose_name='点击次数')
    is_recommend = models.BooleanField(default=False,verbose_name='是否推荐')
    date_publish = models.DateField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户')
    category = models.ForeignKey(Catagory,on_delete=models.CASCADE,blank=True,null=True,verbose_name='分类')
    tag = models.ManyToManyField(Tag,verbose_name='标签')

    objects = ArticleManager()

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title

#评论模型
class Comment(models.Model):
    content = models.TextField(verbose_name='评论内容')
    username = models.CharField(max_length=30,blank=True,null=True,verbose_name='用户名')
    email = models.EmailField(max_length=50,blank=True,null=True,verbose_name='地址邮箱')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='个人网页地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,verbose_name='用户')
    article = models.ForeignKey(Article,on_delete=models.CASCADE,blank=True,null=True,verbose_name='文章')
    pid = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,verbose_name='父级评论')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)

#友情连接的模型
class Links(models.Model):
    title = models.CharField(max_length=50,verbose_name='标题')
    description = models.CharField(max_length=200,verbose_name='友情连接描述')
    callback_url = models.URLField(verbose_name='url地址')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排序顺序(从小到大)')

    class Meta:
        verbose_name = '友情连接'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __unicode__(self):
        return self.title

#广告
class AD(models.Model):
    title = models.CharField(max_length=50,verbose_name='广告歌词')
    description = models.CharField(max_length=200,verbose_name='广告描述')
    image_url = models.ImageField(upload_to='ad/%Y/%m',verbose_name='图片路径')
    callback_url = models.URLField(null=True,blank=True,verbose_name='回调url')
    date_publish = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    index = models.IntegerField(default=999,verbose_name='排列顺序(从小到大)')

    class Meta:
        verbose_name = '广告'
        verbose_name_plural = verbose_name
        ordering = ['index','id']

    def __unicode__(self):
        return self.title