from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout,login,authenticate
from django.conf import settings
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
# Create your views here.
from .models import *
from django.db import connection
from django.db.models import Count
from .forms import CommentForm,RegForm,LoginForm

def global_setting(request):

    SITE_NAME=settings.SITE_NAME
    SITE_DESC=settings.SITE_DESC

    # 分类信息的获取（导航数据）
    catagory_list = Catagory.objects.all()

    # 广告数据
    ad_list = AD.objects.all()

    # 文章归档
    # 1、首先获取文章中有的    年份-月份   2019/11文章归档
    # cursor=connection.cursor()
    # cursor.execute("SELECT DISTINCT DATE_FORMAT(date_publish,'%Y-%m') as col_date FROM blog_article ORDER BY date_publish")
    # row = cursor.fetchall()
    # print(row)
    archive_list = Article.objects.distinct_date()

    #友情链接
    #文章排行榜数据
    #评论排行
    comment_count_list=Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    article_comment_list=[Article.objects.get(pk=comment['article'])for comment in comment_count_list]

    return locals()


def index(request):
    #最新文章数据
    article_list=Article.objects.all()
    article_list=getPage(request,article_list)

    return render(request,'index.html',locals())

def archive(request):
    #先获取客户端提交的信息
    year = request.GET.get('year',None)
    month = request.GET.get('month', None)
    #模糊查询
    article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
    article_list = getPage(request,article_list)


    return render(request, 'archive.html', locals())

#分页代码
def getPage(request,article_list):

    paginator = Paginator(article_list, 1)
    # 分页异常
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list

#文章详情
def article(request):
    #获取文章id
    id = request.GET.get('id',None)
    try:
        #获取文章信息
        article=Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return render(request,'failure.html',{'reason':'没有找到相应的文章'})


    #创建评论表单对象
    comment_form = CommentForm({
                                'author':request.user.username,
                                'email':request.user.email,
                                'url':request.user.url,
                                'article':id} if request.user.is_authenticated else {'article':id})

    #获取评论信息
    comments = Comment.objects.filter(article=article).order_by('id')
    comment_list = []
    for comment in comments:
        for item in comment_list:
            if not hasattr(item,'children_comment'):
                setattr(item,'children_comment',[])
            if comment.pid == item:
                item.children_comment.append(comment)
                break
        if comment.pid is None:
            comment_list.append(comment)



    return render(request, 'article.html',locals())

#提交评论
def comment_post(request):
    comment_from = CommentForm(request.POST)
    if comment_from.is_valid():
        # 获取表单信息
        comment = Comment.objects.create(
                                        username = comment_from.cleaned_data["author"],
                                        email = comment_from.cleaned_data["email"],
                                        url=comment_from.cleaned_data["url"],
                                        content=comment_from.cleaned_data["comment"],
                                        article_id=comment_from.cleaned_data["article"],
                                        user=request.user if request.user.is_authenticated else None)

        comment.save()
    else:
        return render(request,'failure.html',{'reason':comment_from.errors})

    return redirect(request.META['HTTP_REFERER'])

#注册
def do_reg(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            #注册
            user = User.objects.create(username=reg_form.cleaned_data["username"],
                                       email=reg_form.cleaned_data["email"],
                                       url=reg_form.cleaned_data["url"],
                                       password=make_password(reg_form.cleaned_data["password"]),)
            user.save()

            #登陆
            user.backend = 'django.contrib.auth.backends.ModelBackend'  #指定默认的登录方式
            login(request,user)
            return redirect(request.POST.get('source_url'))
        else:
            return render(request,'failure.html',{'reason':reg_form.errors})
    else:
        reg_form = RegForm()

    return render(request,'reg.html',locals())


#登陆
def do_login(request):
    if request.method =='POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():

            #登陆
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username,password=password)
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录方式
                login(request, user)
            else:
                return render(request,'failure.html',{'reason':'登陆验证失败'})

            return redirect(request.POST.get('source_url'))

        else:
            return render(request,'failure.html',{'reason':login_form.errors})
    else:
        login_form = LoginForm()

    return render(request,'login.html',locals())



#注销
def do_logout(request):
    logout(request)
    return redirect(request.META['HTTP_REFERER'])